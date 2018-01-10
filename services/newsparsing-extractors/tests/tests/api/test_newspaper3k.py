'''
Created on 6 janv. 2018

@author: tuco
'''
import unittest

from flask import json

from core.newsparsing.extractors.config.application import get_extractors_fields
from core.newsparsing.extractors.constants.extractors import NEWSPAPER3K
from tests.api import FlaskTestCase


class Newspaper3kTestCase(unittest.TestCase, FlaskTestCase):

    TEST_URL = "http://edition.cnn.com/2013/11/27/justice/tucson-arizona-captive-girls/"
    TEST_EXTRACTOR = NEWSPAPER3K
    
    def setUp(self):
        unittest.TestCase.setUp(self)
        FlaskTestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)
        FlaskTestCase.tearDown(self)

    def test_post(self):
        # Wrong extractor
        response = self.client.post('/extractor/error/extract',
                                    data=json.dumps({
                                        'fields': get_extractors_fields(self.TEST_EXTRACTOR),
                                    }),
                                    headers=self.get_api_headers())
        self.assertResponseCode(response, 403)

        # Empty fields
        response = self.client.post('/extractor/%s/extract' % self.TEST_EXTRACTOR,
                                    data=json.dumps({}),
                                    headers=self.get_api_headers())
        self.assertResponseCode(response, 403)

    def test_newspaper3k(self):
        # Empty url
        response = self.client.post('/extractor/%s/extract' % self.TEST_EXTRACTOR,
                                    data=json.dumps({
                                        'fields': get_extractors_fields(self.TEST_EXTRACTOR)
                                    }),
                                    headers=self.get_api_headers())
        self.assertResponseCode(response, 403)

        # Test extract
        response = self.client.post('/extractor/%s/extract' % self.TEST_EXTRACTOR,
                                    data=json.dumps({
                                        'fields': get_extractors_fields(self.TEST_EXTRACTOR),
                                        'url': self.TEST_URL
                                    }),
                                    headers=self.get_api_headers())
        self.assertResponseCode(response, 200)
