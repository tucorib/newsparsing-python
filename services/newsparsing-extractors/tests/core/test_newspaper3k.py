'''
Created on 5 janv. 2018

@author: tuco
'''
import unittest

from core import ExtractorsTestCase
from newsparsing.extractors.core.config.application import get_extractors_fields
from newsparsing.extractors.core.constants.extractors import NEWSPAPER3K
from newsparsing.extractors.core.errors import MissingMessageKeyException
from newsparsing.extractors.core.extracts import ExtracterActor


class CoreNewspaper3kTestCase(unittest.TestCase, ExtractorsTestCase):

    TEST_EXTRACTOR = NEWSPAPER3K
    TEST_URL = "http://edition.cnn.com/2013/11/27/justice/tucson-arizona-captive-girls/"

    def setUp(self):
        unittest.TestCase.setUp(self)
        ExtractorsTestCase.setUp(self)
        self.TEST_FIELDS = get_extractors_fields(self.TEST_EXTRACTOR)
        self.extracter_actor = ExtracterActor.start()

    def tearDown(self):
        self.extracter_actor.stop()
        unittest.TestCase.tearDown(self)

    def get_expected_fields(self):
        return ['title', 'text', 'authors']

    def test_no_url(self):
        with self.assertRaises(MissingMessageKeyException) as error:
            self.extracter_actor.ask({'extractor': self.TEST_EXTRACTOR,
                                      'fields': self.TEST_FIELDS})
        self.assertEqual(str(error.exception),
                         'Missing key url',
                         'Wrong error raised')

    def text_extract(self):
        for fields in self.get_fields_permutations():
            extracter_result = self.extracter_actor.ask({'extractor': self.TEST_EXTRACTOR,
                                                         'fields': self.TEST_FIELDS,
                                                         'url': self.TEST_URL})
            self.assertExtractedFields(fields, extracter_result)
