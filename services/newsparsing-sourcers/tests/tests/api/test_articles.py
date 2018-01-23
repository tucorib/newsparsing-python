'''
Created on 7 janv. 2018

@author: tuco
'''
from _io import BytesIO
import unittest

from flask import json
import ijson

from tests.api import FlaskTestCase


class FlaskArticlesTestCase(unittest.TestCase, FlaskTestCase):

    TEST_UNKNOWN_SOURCE = 'unknown-source'
    TEST_NO_SOURCER = 'no-sourcer'
    TEST_NO_URL = 'no-url'
    TEST_UNKNOWN_SOURCER = 'unknown-sourcer'

    TEST_SOURCE = 'test'

    def setUp(self):
        unittest.TestCase.setUp(self)
        FlaskTestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)
        FlaskTestCase.tearDown(self)

    def __get_articles(self, response):
        return ijson.items(BytesIO(response.data), 'item')

    def test_unknown_source(self):
        response = self.client.get('/source/%s/articles' % self.TEST_UNKNOWN_SOURCE,
                                   headers=self.get_api_headers())
        self.assertResponseCode(response, 500)
        self.assertDictEqual(json.loads(response.data),
                             {'error': 'Unknown source %s' % self.TEST_UNKNOWN_SOURCE},
                             'Wrong error message')

    def test_no_sourcer(self):
        response = self.client.get('/source/%s/articles' % self.TEST_NO_SOURCER,
                                   headers=self.get_api_headers())
        self.assertResponseCode(response, 500)
        self.assertDictEqual(json.loads(response.data),
                             {'error': 'Source %s has no sourcer' % self.TEST_NO_SOURCER},
                             'Wrong error message')

    def test_no_url(self):
        response = self.client.get('/source/%s/articles' % self.TEST_NO_URL,
                                   headers=self.get_api_headers())
        self.assertResponseCode(response, 500)
        self.assertDictEqual(json.loads(response.data),
                             {'error': 'Source %s has no url' % self.TEST_NO_URL},
                             'Wrong error message')

    def test_unknown_sourcer(self):
        response = self.client.get('/source/%s/articles' % self.TEST_UNKNOWN_SOURCER,
                                   headers=self.get_api_headers())
        self.assertResponseCode(response, 500)
        self.assertDictEqual(json.loads(response.data),
                             {'error': 'Source %s has an unknown sourcer' % self.TEST_UNKNOWN_SOURCER},
                             'Wrong error message')

    def test_source(self):
        response = self.client.get('/source/%s/articles' % self.TEST_SOURCE,
                                   headers=self.get_api_headers())
        self.assertResponseCode(response, 200)

        for article in self.__get_articles(response):
            self.assertEqual(article['source'],
                             self.TEST_SOURCE,
                             'Returned article has wrong source')
            self.assertIn('id',
                          article,
                          'Article has no id')
            self.assertIn('url',
                          article,
                          'Article has no url')

    def test_source_limit(self):
        for limit in range(0, 10):
            response = self.client.get('/source/%s/articles/%d' % (self.TEST_SOURCE, limit),
                                       headers=self.get_api_headers())
            self.assertResponseCode(response, 200)

            article_count = 0
            for article in self.__get_articles(response):
                self.assertEqual(article['source'],
                                 self.TEST_SOURCE,
                                 'Returned article has wrong source')
                self.assertIn('id',
                              article,
                              'Article has no id')
                self.assertIn('url',
                              article,
                              'Article has no url')

                article_count += 1

                self.assertLessEqual(article_count, limit, 'Wrong count returned')
