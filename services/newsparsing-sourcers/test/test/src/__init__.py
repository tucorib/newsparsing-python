from newsparsing.sourcers.config.application import load
import os


class SourcersTest():

    APPLICATION_CONFIGURATION = os.path.join(os.path.dirname(__file__), "../../../conf/test.application.conf")
        
    def setUp(self):
        # Load configuration
        load(self.APPLICATION_CONFIGURATION)