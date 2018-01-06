'''
Created on 5 janv. 2018

@author: tuco
'''
from test.api import ApiTest
import json
import unittest
from newsparsing.sourcers import SourceType


class TestArticles(unittest.TestCase, ApiTest):
    
    def setUp(self):
        ApiTest.setUp(self)
        
    def test_get(self):
        # Unexisting source type
        response = self.client.get('/articles/%s/%s' % ('error', 'lorem-rss'))
        self.assertResponseCode(response, 404)
        
        # Unexisting source name
        response = self.client.get('/articles/%s/%s' % (SourceType.RSS, 'error'))
        self.assertResponseCode(response, 404)
        
        # Get articles
        response = self.client.get('/articles/%s/%s' % (SourceType.RSS, 'lorem-rss'))
        self.assertResponseCode(response, 200)
        for article in json.loads(response.data):
            self.assertDictEqual(article['source'], { 'type': SourceType.RSS, 'name': 'lorem-rss'}, 'Returned article has wrong source')
            self.assertIn('id', article, 'Article has no id')
            self.assertIn('url', article['content'], 'Article has no url')