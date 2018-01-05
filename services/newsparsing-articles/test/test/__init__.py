from newsparsing.articles.config.application import load
import os


class ArticlesTest():

    APPLICATION_CONFIGURATION = os.path.join(os.path.dirname(__file__), "../../conf/application.conf")
        
    def setUp(self):
        # Load configuration
        load(self.APPLICATION_CONFIGURATION)
