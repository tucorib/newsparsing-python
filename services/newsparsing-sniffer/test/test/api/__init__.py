from test import SnifferTest
from api.newsparsing.sniffer.app import create_app
import datetime
import os


class ApiTest(SnifferTest):
    
    FLASK_CONFIGURATION_FILE = os.path.join(os.path.dirname(__file__), "../../../conf/test.flask.conf")
    
    def setUp(self):
        SnifferTest.setUp(self)
        self.flask_app = create_app(self.FLASK_CONFIGURATION_FILE)
        self.flask_app.config['TESTING'] = True
        self.client = self.flask_app.test_client()
        
    def assertResponseCode(self, response, status_code):
        self.assertEqual(response.status_code, status_code, 'Unexpected response status code: %d' % response.status_code)
