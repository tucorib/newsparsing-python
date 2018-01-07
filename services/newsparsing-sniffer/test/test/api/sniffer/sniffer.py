'''
Created on 6 janv. 2018

@author: tuco
'''
from test.api import ApiTest
import unittest
import ijson
from _io import BytesIO


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

        for article in ijson.items(BytesIO(response.data), 'item'):
            self.assertEqual(article['source'], { 'type': self.TEST_SOURCE_TYPE, 'name': self.TEST_SOURCE_NAME}, 'Returned article has wrong source')
            self.assertIn('id', article, 'Article has no id')
            self.assertIn('url', article['content'], 'Article has no url')