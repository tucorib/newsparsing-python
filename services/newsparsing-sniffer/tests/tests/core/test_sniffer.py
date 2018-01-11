'''
Created on 6 janv. 2018

@author: tuco
'''

import unittest

from core.newsparsing.sniffer.articles_sniffer import ArticlesSnifferActor
from core.newsparsing.sniffer.config.application import get_source_fields
from tests.core import CoreSnifferTestCase


class SnifferTestCase(unittest.TestCase, CoreSnifferTestCase):

    TEST_SOURCE = "slate"

    def setUp(self):
        unittest.TestCase.setUp(self)
        CoreSnifferTestCase.setUp(self)

    def test_sniff(self):
        # Create iterator
        articles_sniffer = ArticlesSnifferActor.start()
        articles_iterator = articles_sniffer.ask({'source': self.TEST_SOURCE})
        # Stop actor
        articles_sniffer.stop()

        # Sniff RSS
        for article in articles_iterator:
            self.assertIn('id', article, 'Article has no id')
            for field in get_source_fields(self.TEST_SOURCE):
                self.assertIn(field, article['content'], 'Missing field %s in article' % field)
