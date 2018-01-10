'''
Created on 6 janv. 2018

@author: tuco
'''

import unittest

from core.newsparsing.sniffer.config.application import get_source_fields
from core.newsparsing.sniffer.sniffer import sniff
from tests.core import CoreSnifferTestCase


class SnifferTestCase(unittest.TestCase, CoreSnifferTestCase):

    TEST_SOURCE_TYPE = "rss"
    TEST_SOURCE_NAME = "slate"

    def setUp(self):
        unittest.TestCase.setUp(self)
        CoreSnifferTestCase.setUp(self)

    def test_sniff(self):
        # Sniff RSS
        for article in sniff(self.TEST_SOURCE_TYPE, self.TEST_SOURCE_NAME):
            self.assertEqual(
                article['source'],
                {
                    'type': self.TEST_SOURCE_TYPE,
                    'name': self.TEST_SOURCE_NAME
                },
                'Returned article has wrong source')
            self.assertIn('id', article, 'Article has no id')
            self.assertIn('url', article, 'Article has no url')
            for field in get_source_fields(self.TEST_SOURCE_TYPE, self.TEST_SOURCE_NAME):
                self.assertIn(field, article, 'Missing firld %s in article' % field)
