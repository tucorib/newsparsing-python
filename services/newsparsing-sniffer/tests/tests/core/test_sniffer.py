'''
Created on 6 janv. 2018

@author: tuco
'''

import unittest

from core.newsparsing.sniffer.config.application import get_source_fields
from core.newsparsing.sniffer.sniffer import sniff
from tests.core import CoreSnifferTestCase


class SnifferTestCase(unittest.TestCase, CoreSnifferTestCase):

    TEST_SOURCE = "slate"

    def setUp(self):
        unittest.TestCase.setUp(self)
        CoreSnifferTestCase.setUp(self)

    def test_sniff(self):
        # Sniff RSS
        for article in sniff(self.TEST_SOURCE):
            self.assertEqual(article['source'], self.TEST_SOURCE, 'Returned article has wrong source')
            self.assertIn('id', article, 'Article has no id')
            for field in get_source_fields(self.TEST_SOURCE):
                self.assertIn(field, article, 'Missing firld %s in article' % field)
