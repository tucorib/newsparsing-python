'''
Created on 9 janv. 2018

@author: nribeiro
'''
from _io import BytesIO
import unittest

import ijson

from core.newsparsing.sniffer.config.application import get_source_fields
from tests.api import FlaskTestCase


class ApiSnifferTestCase(unittest.TestCase, FlaskTestCase):

    TEST_SOURCE = "test"

    def setUp(self):
        unittest.TestCase.setUp(self)
        FlaskTestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)
        FlaskTestCase.tearDown(self)

    @classmethod
    def setUpClass(cls):
        FlaskTestCase.setUpClass()
         
    @classmethod
    def tearDownClass(cls):
        FlaskTestCase.tearDownClass()
    
    def test_get(self):
        # Empty extractor
        response = self.client.get('/sniff/%s' % self.TEST_SOURCE)
        self.assertResponseCode(response, 200)

        for article in ijson.items(BytesIO(response.data), 'item'):
            self.assertIn('id', article, 'Article has no id')
            for field in get_source_fields(self.TEST_SOURCE):
                self.assertIn(field, article['content'], 'Missing field %s in article' % field)
