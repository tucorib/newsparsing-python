import os
import unittest

from celery.app.base import Celery
from celery.bin import worker
from celery.bin.celeryd_detach import detached_celeryd

from api.newsparsing.extractors.celery_app import celery, \
    load_celery_configuration
from api.newsparsing.extractors.flask_app import load_flask_configuration
from tests import CONFIG_DIR


class CeleryTestCase():

    APPLICATION_CONFIGURATION = os.path.join(CONFIG_DIR,
                                             "test.application.conf")
    FLASK_CONFIGURATION_FILE = os.path.join(CONFIG_DIR,
                                            "test.flask.conf")
    CELERY_CONFIGURATION_FILE = os.path.join(CONFIG_DIR,
                                             "test.celery.conf")

    def setUp(self):
        # Celery app
        self.celery_app = celery

        # Start worker
        self.worker = self.celery_app.Worker(**{
            '--application-config': self.APPLICATION_CONFIGURATION,
            '--flask-config': self.FLASK_CONFIGURATION_FILE,
            '--celery-config': self.CELERY_CONFIGURATION_FILE,
        })
