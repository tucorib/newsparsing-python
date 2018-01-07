import os
import unittest

from api.newsparsing.sourcers.celery_app import celery, \
    load_celery_configuration
from api.newsparsing.sourcers.flask_app import load_flask_configuration
from tests import CONFIG_DIR
from tests.core import SourcersTestCase


class CeleryTestCase(SourcersTestCase):
    
    FLASK_CONFIGURATION_FILE = os.path.join(CONFIG_DIR, "test.flask.conf")
    CELERY_CONFIGURATION_FILE = os.path.join(CONFIG_DIR, "test.celery.conf")
    
    def setUp(self):
        unittest.TestCase.setUp(self)
        SourcersTestCase.setUp(self)
    
        # Celery app
        self.celery_app = celery
        # Load Flask configuration
        load_flask_configuration(self.celery_app.flask_app, self.FLASK_CONFIGURATION_FILE)
        # Flask TESTING flag
        self.celery_app.flask_app.config['TESTING'] = True
        # Load celery configuration
        load_celery_configuration(self.CELERY_CONFIGURATION_FILE)
    