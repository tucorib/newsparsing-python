'''
Created on 7 janv. 2018

@author: tuco
'''
from _io import BytesIO
import unittest

import ijson
from tests.api import FlaskTestCase


class ArticlesTestCase(unittest.TestCase, FlaskTestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        FlaskTestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)
        FlaskTestCase.tearDown(self)

    def __get_articles(self, response):
        return ijson.items(BytesIO(response.data), 'item')

    def test_404(self):
        # Unexisting source name
        response = self.client.get('/articles/%s' % 'error',
                                   headers=self.get_api_headers())
        self.assertResponseCode(response, 404)

    def test_get_rss(self):
        # Get articles
        response = self.client.get('/articles/%s' % 'slate',
                                   headers=self.get_api_headers())
        self.assertResponseCode(response, 200)

        for article in self.__get_articles(response):
            self.assertEqual(article['source'], 'slate', 'Returned article has wrong source')
            self.assertIn('id', article, 'Article has no id')
            self.assertIn('url', article, 'Article has no url')
