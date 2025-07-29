import json
import signal
import logging
import os
import subprocess
import time
from contextlib import contextmanager
from datetime import datetime
from urllib.error import (
    HTTPError,
    URLError,
)
from urllib.request import urlopen

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.management import load_command_class
from django.utils.autoreload import DJANGO_AUTORELOAD_ENV

_COMPONENTS_LIST_COMMAND = "gcloud components list --format=json".split()
_REQUIRED_COMPONENTS = set(["beta", "cloud-datastore-emulator", "core"])


logger = logging.getLogger(__name__)


@contextmanager
def root_logger_level(level):
    """ Context manager for temporarily changing the root logging level.
        This is to allow logging.info() calls to be surfaced during setup but silenced again during
        the actual running of the tests.
    """
    root_logger = logging.getLogger()
    original_level = root_logger.level
    root_logger.setLevel(logging.INFO)
    # Set the level on the handlers as well, which seems to be necessary
    original_handler_levels = {}
    for handler in root_logger.handlers:
        original_handler_levels[id(handler)] = handler.level
        handler.setLevel(level)
    try:
        yield
    finally:
        root_logger.setLevel(original_level)
        for handler in root_logger.handlers:
            try:
                handler.setLevel(original_handler_levels[id(handler)])
            except KeyError:
                # This handler didn't exist when we changed the levels
                pass


class BaseRunner:
    EMULATOR_HOST = "127.0.0.1"
    PROJECT_ID = "test"
    RUNNER_TYPE = ""

    def __init__(self, *args, **kwargs):
        kwargs['port'] = kwargs.get('port') or self._DEFAULT_EMULATOR_PORT
        for attr, val in kwargs.items():
            setattr(self, attr, val)
        self._process = None
        self._process_output_file_path = f"{self.RUNNER_TYPE}-emulator-output.txt"
        self._process_output_file = open(self._process_output_file_path, "w")

    def execute(self, *args, **kwargs):
        if os.environ.get(DJANGO_AUTORELOAD_ENV) != "true":
            with root_logger_level(logging.INFO):
                self._check_gcloud_components()
                self._start_emulator(**kwargs)

    def _check_gcloud_components(self):
        finished_process = subprocess.run(_COMPONENTS_LIST_COMMAND, stdout=subprocess.PIPE, encoding="utf-8")
        installed_components = set(
            [cp["id"] for cp in json.loads(finished_process.stdout) if cp["current_version_string"] is not None]
        )

        if not self._REQUIRED_COMPONENTS.issubset(installed_components):
            raise RuntimeError(
                "Missing Google Cloud SDK component(s): {}\n"
                "Please run `gcloud components install` to install missing components.".format(
                    ", ".join(self._REQUIRED_COMPONENTS - installed_components)
                )
            )

    def _get_args(self, **kwargs):
        return ["--host-port=127.0.0.1:%s" % self.port]

    def _wait_for_emulator(self, **kwargs):
        TIMEOUT = 60.0

        start = datetime.now()

        def _abort_if_hit_timeout():
            if (datetime.now() - start).total_seconds() > TIMEOUT:
                self._print_process_output()
                raise RuntimeError(
                    f"Unable to start Cloud {self.RUNNER_TYPE.title()} Emulator. "
                    "Please check the output above."
                )

        logger.info("Waiting for Cloud Firestore Emulator...")
        time.sleep(1)

        failures = 0
        while True:
            try:
                response = urlopen("http://127.0.0.1:%s/" % self.port)
            except (HTTPError, URLError):
                _abort_if_hit_timeout()
                failures += 1
                time.sleep(1)
                if failures > 5:
                    # Only start logging if this becomes persistent
                    logger.exception(
                        "Error connecting to the Cloud %s Emulator. Retrying...",
                        self.RUNNER_TYPE.title()
                    )
                continue

            if response.status == 200:
                # Give things a second to really boot
                time.sleep(2)
                break

            _abort_if_hit_timeout()
            time.sleep(1)

    def _start_emulator(self, **kwargs):

        logger.info("Starting Cloud %s Emulator", self.RUNNER_TYPE.title())

        os.environ[self.EMULATOR_HOST_ENV] = "127.0.0.1:%s" % self.port
        os.environ[self.EMULATOR_PROJECT_ID_ENV] = "test"

        # The Cloud Firestore emulator regularly runs out of heap space
        # so set a higher max
        os.environ["JDK_JAVA_OPTIONS"] = "-Xms512M -Xmx1024M"

        env = os.environ.copy()
        self._process = subprocess.Popen(
            self._BASE_COMMAND + self._get_args(**kwargs),
            env=env,
            stdout=self._process_output_file,
            stderr=subprocess.STDOUT,  # Put stderr on the same pipe as stdout
            universal_newlines=True,  # Make the file a text (not bytes) file
        )

        self._wait_for_emulator(**kwargs)

    def _stop_emulator(self):
        logger.info("Stopping Cloud %s Emulator", self.RUNNER_TYPE.title())
        if self._process:
            self._process.terminate()
            self._process.wait()
            self._process = None
        self._process_output_file.close()
        os.unlink(self._process_output_file_path)

    def _print_process_output(self):
        logger.error("=== %s ===", self._process_output_file_path)
        with open(self._process_output_file, "r") as file:
            file.seek(0)
            logger.error(file.read())
        logger.error("=== EOF ===")


class CloudFirestoreRunner(BaseRunner):
    RUNNER_TYPE = 'firestore'
    RUNNER_PARAM_PREFIX = RUNNER_TYPE + "_"
    _DEFAULT_EMULATOR_PORT = 8080
    EMULATOR_HOST_ENV = "FIRESTORE_EMULATOR_HOST"
    EMULATOR_PROJECT_ID_ENV = "FIRESTORE_PROJECT_ID"
    _REQUIRED_COMPONENTS = set(["beta", "cloud-firestore-emulator", "core"])
    _BASE_COMMAND = "gcloud beta emulators firestore start --project=test".split()  # noqa

    def _stop_emulator(self, **kwargs):
        logger.info("Stopping Cloud Firestore Emulator")
        if self._process:
            os.killpg(os.getpgid(self._process.pid), signal.SIGKILL)
            self._process = None
        self._process_output_file.close()
        os.unlink(self._process_output_file_path)


class CloudDatastoreRunner(BaseRunner):
    USE_MEMORY_DATASTORE_BY_DEFAULT = False
    RUNNER_TYPE = 'datastore'
    RUNNER_PARAM_PREFIX = RUNNER_TYPE + "_"
    _DEFAULT_EMULATOR_PORT = 9090
    EMULATOR_HOST_ENV = "DATASTORE_EMULATOR_HOST"
    EMULATOR_PROJECT_ID_ENV = "DATASTORE_PROJECT_ID"
    _REQUIRED_COMPONENTS = set(["beta", "cloud-datastore-emulator", "core"])
    _BASE_COMMAND = "gcloud beta emulators datastore start --no-user-output-enabled --use-firestore-in-datastore-mode --quiet --project=test".split()  # noqa

    def _datastore_filename(self):
        BASE_DIR = getattr(settings, "BASE_DIR", None)

        if not BASE_DIR:
            raise ImproperlyConfigured("Please define BASE_DIR in your Django settings")

        return os.path.join(BASE_DIR, ".datastore")

    def _get_args(self, **kwargs):
        args = super()._get_args(**kwargs)

        if self.use_memory:
            logger.info("Using in-memory datastore")
            args.append("--no-store-on-disk")
        else:
            args.append("--data-dir=%s" % self._datastore_filename())

        return args


def locate_command(name):
    """
        Apps may override Django commands, what we want to do is
        subclass whichever one had precedence before the gcloudc.commands app and subclass that
    """

    try:
        index = settings.INSTALLED_APPS.index("gcloudc.commands")
    except ValueError:
        raise ImproperlyConfigured("Unable to locate gcloudc.commands in INSTALLED_APPS")

    APPS_TO_CHECK = list(settings.INSTALLED_APPS) + ["django.core"]

    for i in range(index + 1, len(APPS_TO_CHECK)):
        app_label = APPS_TO_CHECK[i]
        try:
            command = load_command_class(app_label, name)
        except ModuleNotFoundError:
            continue

        if command:
            return command.__class__
    else:
        raise ImportError("Unable to locate a base %s Command to subclass" % name)


RUNNERS = {
    CloudDatastoreRunner.RUNNER_TYPE: CloudDatastoreRunner,
    CloudFirestoreRunner.RUNNER_TYPE: CloudFirestoreRunner,
}


class RunnerWrapper:
    """ A mixin for Django management commands which starts and stops the necessary Datastore and/or
        Firestore emulators when the command runs.
        Note that similar code exists in `djangae.sandbox` and `manage.py` in the sister projects
        Djangae and Djangae Scaffold respectively. Perhaps these could be consolidated.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._engines = set([db_conf['ENGINE'] for _, db_conf in settings.DATABASES.items()])
        self.runners = [el.split('.')[-1] for el in self._engines]
        self.runner_instances = []

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument("--no-firestore", action="store_false", dest="firestore", default=True)
        parser.add_argument("--no-datastore", action="store_false", dest="datastore", default=True)
        parser.add_argument("--firestore-port", action="store", dest="firestore_port")
        parser.add_argument("--datastore-port", action="store", dest="datastore_port")
        parser.add_argument("--use-memory-datastore", action="store_true", dest="datastore_use_memory")

    def _prepare_runner_args(self, prefix, **kwargs):
        return {
            arg_key.replace(prefix, ''): arg_val
            for arg_key, arg_val in kwargs.items() if arg_key.startswith(prefix)
        }

    def execute(self, *args, **kwargs):
        # exclude firestore
        if not kwargs['firestore']:
            self._engines.remove('gcloudc.db.backends.firestore')
        # exclude datastore
        if not kwargs['datastore']:
            self._engines.remove('gcloudc.db.backends.datastore')
        try:
            for runner in self.runners:
                runner_cls = RUNNERS.get(runner)
                if runner_cls:
                    runner_kwargs = self._prepare_runner_args(runner_cls.RUNNER_PARAM_PREFIX, **kwargs)
                    runner_instance = runner_cls(**runner_kwargs)
                    self.runner_instances.append(runner_instance)
                    runner_instance.execute()

            super().execute(*args, **kwargs)
        finally:
            for instance in self.runner_instances:
                instance._stop_emulator()
