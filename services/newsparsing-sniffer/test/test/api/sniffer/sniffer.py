'''
Created on 6 janv. 2018

@author: tuco
'''
from test.api import ApiTest
import unittest
from flask import json


class TestSniff(unittest.TestCase, ApiTest):
    
    TEST_SOURCE_TYPE = "rss"
    TEST_SOURCE_NAME = "lorem-rss"
    
    def setUp(self):
        ApiTest.setUp(self)
        
    def test_get(self):
        # Empty extractor
        response = self.client.get('/sniff/%s/%s' % (self.TEST_SOURCE_TYPE,
                                                     self.TEST_SOURCE_NAME))
        self.assertResponseCode(response, 200)
        data = json.loads(response.data)
        self.assertIn('articles', data, "Response does not contain 'articles'")
        
