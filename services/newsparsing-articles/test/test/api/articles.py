'''
Created on 5 janv. 2018

@author: tuco
'''
import datetime
import time
from test.api import ApiTest
from api.newsparsing.articles.app import create_app
from flask import json

    
class ArticlesFlaskTest(ApiTest):
    
    def __init__(self, flask_configuration, methodName='runTest'):
        ApiTest.__init__(self, methodName=methodName)
        self.flask_app = create_app(flask_configuration)
        self.flask_app.config['TESTING'] = True
        self.client = self.flask_app.test_client()
    
    def setUp(self):
        self.client.delete('/article/%s' % self.get_test_id())
        
    def get_test_id(self):
        return 'test'
    
    def get_test_content(self):
        return {'published': datetime.datetime.utcnow().replace(microsecond=0).timestamp()}


class TestArticleRun(ArticlesFlaskTest):
    
    def runTest(self):
        response = self.client.get('/article')
        self.assertResponseCode(response, 405)

        
class TestArticlePut(ArticlesFlaskTest):
    
    def runTest(self):
        # Empty
        response = self.client.post('/article',
                                    data=json.dumps({}),
                                    headers={'Content-Type': 'application/json'})
        self.assertResponseCode(response, 403)
        
        # No id
        response = self.client.post('/article',
                                    data=json.dumps({
                                        'content': self.get_test_content()
                                        }),
                                    headers={'Content-Type': 'application/json'})
        self.assertResponseCode(response, 403)
        
        # No content
        response = self.client.post('/article',
                                    data=json.dumps({
                                        'id': self.get_test_id(),
                                        }),
                                    headers={'Content-Type': 'application/json'})
        self.assertResponseCode(response, 403)
        
        # Full
        response = self.client.post('/article',
                                    data=json.dumps({
                                        'id': self.get_test_id(),
                                        'content': self.get_test_content()
                                        }),
                                    headers={'Content-Type': 'application/json'})
        self.assertResponseCode(response, 201)

            
class TestArticleGetWithId(ArticlesFlaskTest):
    
    def runTest(self):
        # Unexisting id
        response = self.client.get('/article/%s' % 'error')
        self.assertResponseCode(response, 404)
        
        # Build content
        content = self.get_test_content()
        # Insert article
        self.client.post('/article',
                         data=json.dumps({
                             'id': self.get_test_id(),
                             'content': content
                             }),
                         headers={'Content-Type': 'application/json'})
        # Get article
        response = self.client.get('/article/%s' % self.get_test_id())
        
        self.assertDictEqual(json.loads(response.data), {'_id': {'_id': self.get_test_id(), 'version': 0}, 'content': content}, 'Test article in DB is not expected: %s' % response.data)

    
class TestArticleGetWithIdVersion(ArticlesFlaskTest):
    
    def runTest(self):
        # Build content
        content = self.get_test_content()
        # Insert article
        self.client.post('/article',
                         data=json.dumps({
                             'id': self.get_test_id(),
                             'content': content
                             }),
                         headers={'Content-Type': 'application/json'})
        # Wait
        time.sleep(1)
        
        # Update article
        response = self.client.put('/article/%s' % self.get_test_id(),
                                   data=json.dumps({
                                       'content': self.get_test_content()
                                       }),
                                   headers={'Content-Type': 'application/json'})
        self.assertResponseCode(response, 200)
        
        # Get first version of article
        response = self.client.get('/article/%s/%d' % (self.get_test_id(), 0))
        
        self.assertDictEqual(json.loads(response.data), {'_id': {'_id': self.get_test_id(), 'version': 0}, 'content': content}, 'Test article in DB is not expected: %s' % response.data)

    
def suite(flask_configuration):
    return [
        TestArticleRun(flask_configuration),
        TestArticlePut(flask_configuration),
        TestArticleGetWithId(flask_configuration),
        TestArticleGetWithIdVersion(flask_configuration)
    ]
