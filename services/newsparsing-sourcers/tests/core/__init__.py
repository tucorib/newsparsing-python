import os

from newsparsing.sourcers.core.config.application import load_configuration


class SourcersTestCase():

    CONFIG_DIR = os.path.join(os.path.dirname(__file__), "../../conf")
    APPLICATION_CONFIGURATION = os.path.join(CONFIG_DIR,
                                             "tests.application.conf")

    def setUp(self):
        # Load configuration
        load_configuration(self.APPLICATION_CONFIGURATION)
