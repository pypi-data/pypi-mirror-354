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
    'default': {
        'ENGINE': 'gcloudc.db.backends.datastore',
        'INDEXES_FILE': os.path.join(os.path.abspath(os.path.dirname(__file__)), "djangaeidx.yaml"),
        "PROJECT": os.getenv("GCLOUDC_PROJECT_ID", default='test'),
        "NAMESPACE": "ns0",  # Use a non-default namespace to catch edge cases where we forget
        "OPTIONS": {
            "count_mode": "emulated",
        }
    },
    "nonamespace": {
        'ENGINE': 'gcloudc.db.backends.datastore',
        'INDEXES_FILE': os.path.join(os.path.abspath(os.path.dirname(__file__)), "djangaeidx.yaml"),
        "PROJECT": os.getenv("GCLOUDC_PROJECT_ID", default='test'),
        "NAMESPACE": "",
        "OPTIONS": {
            "count_mode": "emulated",
        }
    },
    "non_default_connection": {
        'ENGINE': 'gcloudc.db.backends.datastore',
        'INDEXES_FILE': os.path.join(os.path.abspath(os.path.dirname(__file__)), "djangaeidx.yaml"),
        "PROJECT": os.getenv("GCLOUDC_PROJECT_ID", default='test'),
        "NAMESPACE": "ns1",  # Use a non-default namespace to catch edge cases where we forget
        "OPTIONS": {
            "count_mode": "emulated",
        }
    },
    "non_default_database": {
        'ENGINE': 'gcloudc.db.backends.datastore',
        'INDEXES_FILE': os.path.join(os.path.abspath(os.path.dirname(__file__)), "djangaeidx.yaml"),
        "PROJECT": os.getenv("GCLOUDC_PROJECT_ID", default='test'),
        "DATABASE_ID": "foo",
        "OPTIONS": {
            "count_mode": "emulated",
        }
    },
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
SECRET_KEY = "secret_key_for_testing"
USE_TZ = True

TEST_RUNNER = "xmlrunner.extra.djangotestrunner.XMLTestRunner"
TEST_OUTPUT_FILE_NAME = ".reports/django-tests.xml"

# Use to route db operations to different dbs
DATABASE_ROUTERS = [
    "gcloudc.tests.router.Router",
]
