'''
Created on 6 janv. 2018

@author: tuco
'''

import unittest

from core.newsparsing.sniffer.config.application import get_source_fields
from core.newsparsing.sniffer.errors import MissingMessageKeyException
from core.newsparsing.sniffer.sniffer import ArticlesSnifferActor
from tests.core import CoreSnifferTestCase, setUpModule as coreSetUpModule, tearDownModule as coreTearDownModule


def setUpModule():
    coreSetUpModule()


def tearDownModule():
    coreTearDownModule()


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

    def test_no_source(self):
        with self.assertRaises(MissingMessageKeyException) as error:
            list(self.articles_sniffer.ask({}))
        self.assertEqual(str(error.exception),
                         'Missing key source',
                         'Wrong error raised')

    def test_unknown_source(self):
        with self.assertRaises(Exception) as error:
            list(self.articles_sniffer.ask({'source': self.TEST_UNKNOWN_SOURCE}))
        self.assertEqual(str(error.exception),
                         'Unknown source %s' % self.TEST_UNKNOWN_SOURCE,
                         'Wrong error raised')

    def test_no_sourcer(self):
        with self.assertRaises(Exception) as error:
            list(self.articles_sniffer.ask({'source': self.TEST_NO_SOURCER}))
        self.assertEqual(str(error.exception),
                         'Source %s has no sourcer' % self.TEST_NO_SOURCER,
                         'Wrong error raised')

    def test_no_url(self):
        with self.assertRaises(Exception) as error:
            list(self.articles_sniffer.ask({'source': self.TEST_NO_URL}))
        self.assertEqual(str(error.exception),
                         'Source %s has no url' % self.TEST_NO_URL,
                         'Wrong error raised')

    def test_unknown_sourcer(self):
        with self.assertRaises(Exception) as error:
            list(self.articles_sniffer.ask({'source': self.TEST_UNKNOWN_SOURCER}))
        self.assertEqual(str(error.exception),
                         'Source %s has an unknown sourcer' % self.TEST_UNKNOWN_SOURCER,
                         'Wrong error raised')

    def test_sniff_yield(self):
        # Create iterator
        articles_iterator = self.articles_sniffer.ask({'source': self.TEST_SOURCE})
        # Sniff RSS
        for article in articles_iterator:
            self.assertIn('id', article, 'Article has no id')
            for field in get_source_fields(self.TEST_SOURCE):
                self.assertIn(field, article['content'], 'Missing field %s in article' % field)

    def test_sniff_store(self):
        # Create iterator
        articles_iterator = self.articles_sniffer.ask({'source': self.TEST_SOURCE,
                                                       'store': True})
        # Sniff RSS
        for article in articles_iterator:
            self.assertIn('id', article, 'Article has no id')
            self.assertIn('version', article, 'Article has no version')
            self.assertEqual(article['version'], 0, 'Wrong version returned')
