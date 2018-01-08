import os

from core.newsparsing.sourcers.config.application import load_configuration
from tests import CONFIG_DIR


class SourcersTestCase():

    APPLICATION_CONFIGURATION = os.path.join(CONFIG_DIR,
                                             "test.application.conf")

    def setUp(self):
        # Load configuration
        load_configuration(self.APPLICATION_CONFIGURATION)
