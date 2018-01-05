from test import ArticlesTest
from api.newsparsing.articles.app import create_app
import datetime
import os


class ApiTest(ArticlesTest):
    
    FLASK_CONFIGURATION_FILE = os.path.join(os.path.dirname(__file__), "../../../conf/test.flask.conf")
    
    def setUp(self):
        ArticlesTest.setUp(self)
        self.flask_app = create_app(self.FLASK_CONFIGURATION_FILE)
        self.flask_app.config['TESTING'] = True
        self.client = self.flask_app.test_client()
        self.client.delete('/article/%s' % self.get_test_id())
        
    def get_test_id(self):
        return 'test'
    
    def get_test_content(self):
        return {'published': datetime.datetime.utcnow().replace(microsecond=0).timestamp()}
    
    def get_api_url(self):
        pass
    
    def get_allowed_methods(self):
        return []
    
    def test_allowed_methods(self):
        for method in ['GET', 'PATCH', 'POST', 'HEAD', 'PUT', 'DELETE', 'OPTIONS', 'TRACE']:
            if not method in self.get_allowed_methods():
                # Test method for API url
                response = self.client.open(method=method)
                self.assertEqual(response.status_code, 404, '%s should not be allowed for URL %s' % (method, self.get_api_url()))
                
    def assertResponseCode(self, response, status_code):
        self.assertEqual(response.status_code, status_code, 'Unexpected response status code: %d' % response.status_code)
