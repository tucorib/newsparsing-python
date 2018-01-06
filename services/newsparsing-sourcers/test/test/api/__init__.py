from test import SourcersTest
from api.newsparsing.sourcers.app import create_app
import datetime
import os


class ApiTest(SourcersTest):
    
    FLASK_CONFIGURATION_FILE = os.path.join(os.path.dirname(__file__), "../../../conf/test.flask.conf")
    
    def setUp(self):
        SourcersTest.setUp(self)
        self.flask_app = create_app(self.FLASK_CONFIGURATION_FILE)
        self.flask_app.config['TESTING'] = True
        self.client = self.flask_app.test_client()
        
    def assertResponseCode(self, response, status_code):
        self.assertEqual(response.status_code, status_code, 'Unexpected response status code: %d' % response.status_code)
