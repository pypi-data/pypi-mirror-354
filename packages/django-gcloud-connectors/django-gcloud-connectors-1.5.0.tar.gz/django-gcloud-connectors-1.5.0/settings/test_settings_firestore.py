import logging
import os

# Shut the logging up
logging.getLogger().setLevel(logging.ERROR)

BASE_DIR = os.path.dirname(__file__)

INSTALLED_APPS = (
    'gcloudc',
    'gcloudc.commands',
    'gcloudc.tests'
)

DATABASES = {
    # The Firestore emulator doesn't (yet) support multiple databases, but it does support multiple
    # projects, so we abuse the "project" param to give us multiple databases.
    'default': {
        'ENGINE': 'gcloudc.db.backends.firestore',
        'INDEXES_FILE': os.path.join(os.path.abspath(os.path.dirname(__file__)), "djangaeidx.yaml"),
        "PROJECT": os.getenv("GCLOUDC_PROJECT_ID", default='ns0'),
    },
    "nonamespace": {
        'ENGINE': 'gcloudc.db.backends.firestore',
        'INDEXES_FILE': os.path.join(os.path.abspath(os.path.dirname(__file__)), "djangaeidx.yaml"),
        "PROJECT": 'test',
    },
    "non_default_connection": {
        'ENGINE': 'gcloudc.db.backends.firestore',
        'INDEXES_FILE': os.path.join(os.path.abspath(os.path.dirname(__file__)), "djangaeidx.yaml"),
        "PROJECT": 'ns1',
    },
    "non_default_database": {
        'ENGINE': 'gcloudc.db.backends.firestore',
        'INDEXES_FILE': os.path.join(os.path.abspath(os.path.dirname(__file__)), "djangaeidx.yaml"),
        "PROJECT": os.getenv("GCLOUDC_PROJECT_ID", default='ns0'),
        "DATABASE_ID": "foo",
    },
}

# Use to route db operations to different dbs
DATABASE_ROUTERS = [
    "gcloudc.tests.router.Router",
]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
SECRET_KEY = "secret_key_for_testing"
USE_TZ = True

TEST_RUNNER = "xmlrunner.extra.djangotestrunner.XMLTestRunner"
TEST_OUTPUT_FILE_NAME = ".reports/django-tests.xml"
