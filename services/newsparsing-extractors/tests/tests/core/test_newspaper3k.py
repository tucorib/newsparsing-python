'''
Created on 5 janv. 2018

@author: tuco
'''
import unittest

from core.newsparsing.extractors.constants.extractors import NEWSPAPER3K
from core.newsparsing.extractors.extracts import ExtracterActor
from tests.core import ExtractorsTestCase


class TestNewspaper3k(unittest.TestCase, ExtractorsTestCase):

    TEST_EXTRACTOR = NEWSPAPER3K
    TEST_URL = "http://edition.cnn.com/2013/11/27/justice/tucson-arizona-captive-girls/"

    def text_extract(self):
        for fields in self.get_fields_permutations():
            # Start actor
            extracter_actor = ExtracterActor.start()
            extracter_result = extracter_actor.ask({'extractor': self.TEST_EXTRACTOR,
                                                    'fields': fields,
                                                    'url': self.TEST_URL})

            # Stop actor
            extracter_actor.stop()

            self.assertExtractedFields(fields, extracter_result)
