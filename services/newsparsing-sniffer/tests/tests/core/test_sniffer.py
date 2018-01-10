'''
Created on 6 janv. 2018

@author: tuco
'''

import aiounittest

from core.newsparsing.sniffer.sniffer import sniff
from tests.core import CoreSnifferTestCase


class SnifferTestCase(aiounittest.AsyncTestCase, CoreSnifferTestCase):

    TEST_SOURCE_TYPE = "rss"
    TEST_SOURCE_NAME = "slate"

    def setUp(self):
        aiounittest.AsyncTestCase.setUp(self)
        CoreSnifferTestCase.setUp(self)

    def test_sniff(self):
        # Sniff RSS
        for article in sniff(self.TEST_SOURCE_TYPE, self.TEST_SOURCE_NAME):
            print(article)
