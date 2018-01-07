'''
Created on 5 janv. 2018

@author: tuco
'''
from test.api import ApiTest
import unittest
from newsparsing.sourcers import SourceType
import ijson
from io import BytesIO


class TestArticles(unittest.TestCase, ApiTest):
    
    TEST_SOURCE_TYPE = SourceType.RSS
    TEST_SOURCE_NAME = "lorem-rss"
    
    def setUp(self):
        ApiTest.setUp(self)
        
    def test_get(self):
        # Unexisting source type
        response = self.client.get('/articles/%s/%s' % ('error',
                                                        self.TEST_SOURCE_NAME))
        self.assertResponseCode(response, 404)
        
        # Unexisting source name
        response = self.client.get('/articles/%s/%s' % (self.TEST_SOURCE_TYPE,
                                                        'error'))
        self.assertResponseCode(response, 404)
        
        # Get articles
        response = self.client.get('/articles/%s/%s' % (self.TEST_SOURCE_TYPE,
                                                        self.TEST_SOURCE_NAME))
        self.assertResponseCode(response, 200)
        
        for article in ijson.items(BytesIO(response.data), 'item'):
            self.assertDictEqual(article['source'], { 'type': self.TEST_SOURCE_TYPE, 'name': self.TEST_SOURCE_NAME}, 'Returned article has wrong source')
            self.assertIn('id', article, 'Article has no id')
            self.assertIn('url', article['content'], 'Article has no url')
