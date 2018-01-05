'''
Created on 5 janv. 2018

@author: tuco
'''
from test.api.articles import ArticlesFlaskTest
from flask import json


class TestArticleId(ArticlesFlaskTest):
    
    def get_api_url(self):
        return '/article/%s' % self.get_test_id()
    
    def get_allowed_methods(self):
        return ['GET', 'PUT', 'DELETE']

    def runTest(self):
        ArticlesFlaskTest.runTest(self)
        
        # Unexisting id
        response = self.client.get('/article/%s' % 'error')
        self.assertResponseCode(response, 404)
        
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
        
        # Get article
        response = self.client.get('/article/%s' % self.get_test_id())
        self.assertResponseCode(response, 200)
        self.assertDictEqual(json.loads(response.data), {'_id': {'_id': self.get_test_id(), 'version': 0}, 'content': content}, 'Test article in DB is not expected: %s' % response.data)
