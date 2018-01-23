'''
Created on 16 janv. 2018

@author: nribeiro
'''
import unittest

from core import ExtractorsTestCase
from newsparsing.extractors.core.config.application import get_extractors_fields
from newsparsing.extractors.core.constants.extractors import NEWSPAPER3K
from newsparsing.extractors.core.errors import MissingMessageKeyException, \
    UnknownExtractorException
from newsparsing.extractors.core.extracts import ExtracterActor


class CoreExtractsTestCase(unittest.TestCase, ExtractorsTestCase):

    TEST_UNKNOWN_EXTRACTOR = 'unknown-extractor'

    TEST_EXTRACTOR = NEWSPAPER3K

    def setUp(self):
        unittest.TestCase.setUp(self)
        ExtractorsTestCase.setUp(self)
        self.TEST_FIELDS = get_extractors_fields(self.TEST_EXTRACTOR)
        self.extracter_actor = ExtracterActor.start()

    def tearDown(self):
        self.extracter_actor.stop()
        unittest.TestCase.tearDown(self)

    def test_missing_extractor_key(self):
        with self.assertRaises(MissingMessageKeyException) as error:
            self.extracter_actor.ask({'fields': self.TEST_FIELDS})
        self.assertEqual(str(error.exception),
                         'Missing key extractor',
                         'Wrong error raised')

    def test_missing_fields_key(self):
        with self.assertRaises(MissingMessageKeyException) as error:
            self.extracter_actor.ask({'extractor': self.TEST_EXTRACTOR})
        self.assertEqual(str(error.exception),
                         'Missing key fields',
                         'Wrong error raised')

    def test_unknwon_extractor(self):
        with self.assertRaises(UnknownExtractorException) as error:
            self.extracter_actor.ask({'extractor': self.TEST_UNKNOWN_EXTRACTOR,
                                      'fields': self.TEST_FIELDS})
        self.assertEqual(str(error.exception),
                         'Unknown extractor %s' % self.TEST_UNKNOWN_EXTRACTOR,
                         'Wrong error raised')
