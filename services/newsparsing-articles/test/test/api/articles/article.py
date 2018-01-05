'''
Created on 5 janv. 2018

@author: tuco
'''
from test.api import ApiTest
import json
import unittest


class TestArticle(unittest.TestCase, ApiTest):
    
    def get_api_url(self):
        return '/article'
    
    def get_allowed_methods(self):
        return ['POST']
    
    def setUp(self):
        ApiTest.setUp(self)
        
    def test_post(self):
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
        