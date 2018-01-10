import os

from core.newsparsing.articles.config.application import load_configuration
from tests import CONFIG_DIR


class ArticlesTestCase():

    APPLICATION_CONFIGURATION = os.path.join(CONFIG_DIR,
                                             "tests.application.conf")

    def setUp(self):
        # Load configuration
        load_configuration(self.APPLICATION_CONFIGURATION)
