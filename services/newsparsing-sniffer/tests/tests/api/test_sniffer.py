'''
Created on 9 janv. 2018

@author: nribeiro
'''
from _io import BytesIO

import aiounittest
import ijson

from tests.api import FlaskTestCase


class ApiSnifferTestCase(aiounittest.AsyncTestCase, FlaskTestCase):

    TEST_SOURCE_TYPE = "rss"
    TEST_SOURCE_NAME = "slate"

    def setUp(self):
        aiounittest.AsyncTestCase.setUp(self)
        FlaskTestCase.setUp(self)

    def tearDown(self):
        aiounittest.AsyncTestCase.tearDown(self)
        FlaskTestCase.tearDown(self)

    def test_get(self):
        # Empty extractor
        response = self.client.get('/sniff/%s/%s' % (self.TEST_SOURCE_TYPE,
                                                     self.TEST_SOURCE_NAME))
        self.assertResponseCode(response, 200)

        for article in ijson.items(BytesIO(response.data), 'item'):
            self.assertEqual(
                article['source'],
                {
                    'type': self.TEST_SOURCE_TYPE,
                    'name': self.TEST_SOURCE_NAME
                },
                'Returned article has wrong source')
            self.assertIn('id', article, 'Article has no id')
            self.assertIn('url', article['content'], 'Article has no url')
