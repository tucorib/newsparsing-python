'''
Created on 6 janv. 2018

@author: tuco
'''
import unittest

from flask import json

from api import FlaskTestCase
from newsparsing.extractors.core.config.application import get_extractors_fields
from newsparsing.extractors.core.constants.extractors import NEWSPAPER3K


class FlaskNewspaper3kTestCase(unittest.TestCase, FlaskTestCase):

    TEST_URL = "http://edition.cnn.com/2013/11/27/justice/tucson-arizona-captive-girls/"
    TEST_EXTRACTOR = NEWSPAPER3K

    def setUp(self):
        unittest.TestCase.setUp(self)
        FlaskTestCase.setUp(self)
        self.TEST_FIELDS = get_extractors_fields(self.TEST_EXTRACTOR)

    def tearDown(self):
        unittest.TestCase.tearDown(self)
        FlaskTestCase.tearDown(self)

    def test_no_url(self):
        response = self.client.post('/extractor/%s/extract' % self.TEST_EXTRACTOR,
                                    data=json.dumps({
                                        'fields': self.TEST_FIELDS,
                                    }),
                                   headers=self.get_api_headers())
        self.assertResponseCode(response, 500)
        self.assertDictEqual(json.loads(response.data),
                             {'error': 'Missing key url'},
                             'Wrong error message')

    def test_extract(self):
        # Test extract
        response = self.client.post('/extractor/%s/extract' % self.TEST_EXTRACTOR,
                                    data=json.dumps({
                                        'fields': self.TEST_FIELDS,
                                        'url': self.TEST_URL
                                    }),
                                    headers=self.get_api_headers())
        self.assertResponseCode(response, 200)
