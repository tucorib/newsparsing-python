'''
Created on 5 janv. 2018

@author: tuco
'''
import unittest

from core.newsparsing.extractors.newspaper3k import extract_fields
from tests.core import ExtractorsTestCase


class TestNewspaper3k(unittest.TestCase, ExtractorsTestCase):

    TEST_URL = "http://edition.cnn.com/2013/11/27/justice/tucson-arizona-captive-girls/"

    def text_extract(self):
        for fields in self.get_fields_permutations():
            extracts = extract_fields(self.TEST_URL,
                                      fields)
            self.assertExtractedFields(fields, extracts)
