'''
Created on 6 janv. 2018

@author: tuco
'''
from test.api import ApiTest
import unittest
from flask import json


class TestExtract(unittest.TestCase, ApiTest):
    
    TEST_EXTRACTOR = "newspaper3k"
    TEST_FIELDS = []
    TEST_URL = ""
    
    def setUp(self):
        ApiTest.setUp(self)
        
    def test_post(self):
        # Empty extractor
        response = self.client.post('/extract',
                                    data=json.dumps({
                                        'fields': self.TEST_FIELDS,
                                    }),
                                    headers={'Content-Type': 'application/json'})
        self.assertResponseCode(response, 403)
        
        # Empty fields
        response = self.client.post('/extract',
                                    data=json.dumps({
                                        'extractor': self.TEST_EXTRACTOR,
                                    }),
                                    headers={'Content-Type': 'application/json'})
        self.assertResponseCode(response, 403)
    
    def test_newspaper3k(self):
        TEST_URL = "http://edition.cnn.com/2013/11/27/justice/tucson-arizona-captive-girls/"
        
        # Empty url
        response = self.client.post('/extract',
                                    data=json.dumps({
                                        'extractor': 'newspaper3k',
                                        'fields': ['title', 'text', 'authors']
                                    }),
                                    headers={'Content-Type': 'application/json'})
        self.assertResponseCode(response, 403)
        
        # Test extract
        response = self.client.post('/extract',
                                    data=json.dumps({
                                        'extractor': 'newspaper3k',
                                        'url': TEST_URL,
                                        'fields': ['title', 'text', 'authors']
                                    }),
                                    headers={'Content-Type': 'application/json'})
        self.assertResponseCode(response, 200)
        