'''
Created on 5 janv. 2018

@author: tuco
'''
from test.api.articles import ArticlesFlaskTest
from flask import json
import time


class TestArticleIdVersion(ArticlesFlaskTest):
    
    def get_api_url(self):
        return '/article/%s/%d' % (self.get_test_id(), 0)
    
    def get_allowed_methods(self):
        return ['GET', 'PUT', 'DELETE']
    
    def runTest(self):
        ArticlesFlaskTest.runTest(self)
        
        # Build content
        content = self.get_test_content()
        # Insert article
        response = self.client.post('/article',
                                    data=json.dumps({
                                        'id': self.get_test_id(),
                                        'content': content
                                        }),
                                    headers={'Content-Type': 'application/json'})
        self.assertResponseCode(response, 201)
        
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
        self.assertResponseCode(response, 200)
        self.assertDictEqual(json.loads(response.data), {'_id': {'_id': self.get_test_id(), 'version': 0}, 'content': content}, 'Test article in DB is not expected: %s' % response.data)
