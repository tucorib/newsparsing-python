'''
Created on 9 janv. 2018

@author: nribeiro
'''
from _io import BytesIO
import unittest

from flask import json
import ijson

from api import FlaskTestCase
from core import setUpModule as coreSetUpModule, tearDownModule as coreTearDownModule
from newsparsing.sniffer.core.config.application import get_source_fields


def setUpModule():
    coreSetUpModule()


def tearDownModule():
    coreTearDownModule()


class ApiSnifferTestCase(unittest.TestCase, FlaskTestCase):

    TEST_UNKNOWN_SOURCE = 'unknown-source'
    TEST_NO_SOURCER = 'no-sourcer'
    TEST_NO_URL = 'no-url'
    TEST_UNKNOWN_SOURCER = 'unknown-sourcer'

    TEST_SOURCE = "test"

    def setUp(self):
        unittest.TestCase.setUp(self)
        FlaskTestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)
        FlaskTestCase.tearDown(self)

    def test_unknown_source(self):
        response = self.client.get('/sniff/%s' % self.TEST_UNKNOWN_SOURCE,
                                   headers=self.get_api_headers())
        self.assertResponseCode(response, 500)
        self.assertDictEqual(json.loads(response.data),
                             {'error': 'Unknown source %s' % self.TEST_UNKNOWN_SOURCE},
                             'Wrong error message')

    def test_no_sourcer(self):
        response = self.client.get('/sniff/%s' % self.TEST_NO_SOURCER,
                                   headers=self.get_api_headers())
        self.assertResponseCode(response, 500)
        self.assertDictEqual(json.loads(response.data),
                             {'error': 'Source %s has no sourcer' % self.TEST_NO_SOURCER},
                             'Wrong error message')

    def test_no_url(self):
        response = self.client.get('/sniff/%s' % self.TEST_NO_URL,
                                   headers=self.get_api_headers())
        self.assertResponseCode(response, 500)
        self.assertDictEqual(json.loads(response.data),
                             {'error': 'Source %s has no url' % self.TEST_NO_URL},
                             'Wrong error message')

    def test_unknown_sourcer(self):
        response = self.client.get('/sniff/%s' % self.TEST_UNKNOWN_SOURCER,
                                   headers=self.get_api_headers())
        self.assertResponseCode(response, 500)
        self.assertDictEqual(json.loads(response.data),
                             {'error': 'Source %s has an unknown sourcer' % self.TEST_UNKNOWN_SOURCER},
                             'Wrong error message')

    def test_sniff_get(self):
        # Empty extractor
        response = self.client.get('/sniff/%s' % self.TEST_SOURCE)
        self.assertResponseCode(response, 200)

        for article in ijson.items(BytesIO(response.data), 'item'):
            self.assertIn('id', article, 'Article has no id')
            for field in get_source_fields(self.TEST_SOURCE):
                self.assertIn(field, article['content'], 'Missing field %s in article' % field)

    def test_sniff_post(self):
        # Empty extractor
        response = self.client.post('/sniff/%s' % self.TEST_SOURCE)
        self.assertResponseCode(response, 200)
