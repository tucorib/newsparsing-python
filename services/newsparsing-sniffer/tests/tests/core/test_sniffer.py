'''
Created on 6 janv. 2018

@author: tuco
'''

import unittest

from core.newsparsing.sniffer.config.application import get_source_fields
from core.newsparsing.sniffer.errors import MissingMessageKeyException
from core.newsparsing.sniffer.sniffer import ArticlesSnifferActor
from tests.core import CoreSnifferTestCase


class SnifferTestCase(unittest.TestCase, CoreSnifferTestCase):

    TEST_UNKNOWN_SOURCE = 'unknown-source'
    TEST_NO_SOURCER = 'no-sourcer'
    TEST_NO_URL = 'no-url'
    TEST_UNKNOWN_SOURCER = 'unknown-sourcer'

    TEST_SOURCE = "test"

    def setUp(self):
        unittest.TestCase.setUp(self)
        CoreSnifferTestCase.setUp(self)
        self.articles_sniffer = ArticlesSnifferActor.start()

    def tearDown(self):
        self.articles_sniffer.stop()
        unittest.TestCase.tearDown(self)

    def setUpModule(self):
        CoreSnifferTestCase.setUpModule(self)
    
    def tearDownModule(self):
        CoreSnifferTestCase.tearDownModule(self)
        
    def test_no_command(self):
        with self.assertRaises(MissingMessageKeyException) as error:
            self.articles_sniffer.ask({'source': self.TEST_UNKNOWN_SOURCE})
        self.assertEqual(str(error.exception),
                         'Missing key command',
                         'Wrong error raised')

    def test_no_source(self):
        with self.assertRaises(MissingMessageKeyException) as error:
            self.articles_sniffer.ask({'command': 'sniff'})
        self.assertEqual(str(error.exception),
                         'Missing key source',
                         'Wrong error raised')

    def test_unknown_source(self):
        with self.assertRaises(Exception) as error:
            self.articles_sniffer.ask({'command': 'sniff',
                                       'source': self.TEST_UNKNOWN_SOURCE})
        self.assertEqual(str(error.exception),
                         'Unknown source %s' % self.TEST_UNKNOWN_SOURCE,
                         'Wrong error raised')

    def test_no_sourcer(self):
        with self.assertRaises(Exception) as error:
            self.articles_sniffer.ask({'command': 'sniff',
                                       'source': self.TEST_NO_SOURCER})
        self.assertEqual(str(error.exception),
                         'Source %s has no sourcer' % self.TEST_NO_SOURCER,
                         'Wrong error raised')

    def test_no_url(self):
        with self.assertRaises(Exception) as error:
            self.articles_sniffer.ask({'command': 'sniff',
                                       'source': self.TEST_NO_URL})
        self.assertEqual(str(error.exception),
                         'Source %s has no url' % self.TEST_NO_URL,
                         'Wrong error raised')

    def test_unknown_sourcer(self):
        with self.assertRaises(Exception) as error:
            self.articles_sniffer.ask({'command': 'sniff',
                                       'source': self.TEST_UNKNOWN_SOURCER})
        self.assertEqual(str(error.exception),
                         'Source %s has an unknown sourcer' % self.TEST_UNKNOWN_SOURCER,
                         'Wrong error raised')

    def test_sniff(self):
        # Create iterator
        articles_iterator = self.articles_sniffer.ask({'command': 'sniff',
                                                       'source': self.TEST_SOURCE})
        # Sniff RSS
        for article in articles_iterator:
            self.assertIn('id', article, 'Article has no id')
            for field in get_source_fields(self.TEST_SOURCE):
                self.assertIn(field, article['content'], 'Missing field %s in article' % field)
