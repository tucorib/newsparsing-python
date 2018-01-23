'''
Created on 16 janv. 2018

@author: nribeiro
'''
import unittest

from flask import json

from api import FlaskTestCase
from newsparsing.extractors.core.config.application import get_extractors_fields
from newsparsing.extractors.core.constants.extractors import NEWSPAPER3K


class FlaskExtractTestCase(unittest.TestCase, FlaskTestCase):

    TEST_UNKNOWN_EXTRACTOR = 'unknown-extractor'

    TEST_EXTRACTOR = NEWSPAPER3K

    def setUp(self):
        unittest.TestCase.setUp(self)
        FlaskTestCase.setUp(self)
        self.TEST_FIELDS = get_extractors_fields(self.TEST_EXTRACTOR)

    def tearDown(self):
        unittest.TestCase.tearDown(self)
        FlaskTestCase.tearDown(self)

    def test_unknown_extractor(self):
        response = self.client.post('/extractor/%s/extract' % self.TEST_UNKNOWN_EXTRACTOR,
                                    data=json.dumps({
                                        'fields': self.TEST_FIELDS,
                                    }),
                                   headers=self.get_api_headers())
        self.assertResponseCode(response, 500)
        self.assertDictEqual(json.loads(response.data),
                             {'error': 'Unknown extractor %s' % self.TEST_UNKNOWN_EXTRACTOR},
                             'Wrong error message')

    def test_no_fields(self):
        response = self.client.post('/extractor/%s/extract' % self.TEST_EXTRACTOR,
                                    data=json.dumps({}),
                                   headers=self.get_api_headers())
        self.assertResponseCode(response, 500)
        self.assertDictEqual(json.loads(response.data),
                             {'error': 'Missing key fields'},
                             'Wrong error message')
