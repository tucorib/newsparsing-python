from test.api import ApiTest
from api.newsparsing.articles.app import create_app
import datetime


class ArticlesFlaskTest(ApiTest):
    
    def __init__(self, flask_configuration):
        ApiTest.__init__(self)
        self.flask_app = create_app(flask_configuration)
        self.flask_app.config['TESTING'] = True
        self.client = self.flask_app.test_client()
    
    def setUp(self):
        self.client.delete('/article/%s' % self.get_test_id())
        
    def get_test_id(self):
        return 'test'
    
    def get_test_content(self):
        return {'published': datetime.datetime.utcnow().replace(microsecond=0).timestamp()}
