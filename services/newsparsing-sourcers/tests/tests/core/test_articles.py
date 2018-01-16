'''
Created on 9 janv. 2018

@author: nribeiro
'''
from _collections_abc import Iterator
import unittest

from core.newsparsing.sourcers.articles import ArticlesActor
from core.newsparsing.sourcers.errors import MissingMessageKeyException, \
    UnknownSourceException, NoSourcerException, NoUrlException, \
    UnknownSourcerException
from tests.core import SourcersTestCase


class CoreArticlesTestCase(unittest.TestCase, SourcersTestCase):

    TEST_UNKNOWN_SOURCE = 'unknown-source'
    TEST_NO_SOURCER = 'no-sourcer'
    TEST_NO_URL = 'no-url'
    TEST_UNKNOWN_SOURCER = 'unknown-sourcer'

    TEST_SOURCE = 'test'

    def setUp(self):
        unittest.TestCase.setUp(self)
        SourcersTestCase.setUp(self)
        self.articles_actor = ArticlesActor.start()

    def tearDown(self):
        self.articles_actor.stop()
        unittest.TestCase.tearDown(self)

    def test_missing_source_key(self):
        with self.assertRaises(MissingMessageKeyException) as error:
            list(self.articles_actor.ask({}))
        self.assertEqual(str(error.exception),
                         'Missing key source',
                         'Wrong error raised')

    def test_unknown_source(self):
        with self.assertRaises(UnknownSourceException) as error:
            list(self.articles_actor.ask({'source': self.TEST_UNKNOWN_SOURCE}))
        self.assertEqual(str(error.exception),
                         'Unknown source %s' % self.TEST_UNKNOWN_SOURCE,
                         'Wrong error raised')

    def test_no_sourcer(self):
        with self.assertRaises(NoSourcerException) as error:
            list(self.articles_actor.ask({'source': self.TEST_NO_SOURCER}))
        self.assertEqual(str(error.exception),
                         'Source %s has no sourcer' % self.TEST_NO_SOURCER,
                         'Wrong error raised')

    def test_no_url(self):
        with self.assertRaises(NoUrlException) as error:
            list(self.articles_actor.ask({'source': self.TEST_NO_URL}))
        self.assertEqual(str(error.exception),
                         'Source %s has no url' % self.TEST_NO_URL,
                         'Wrong error raised')

    def test_unknown_sourcer(self):
        with self.assertRaises(UnknownSourcerException) as error:
            list(self.articles_actor.ask({'source': self.TEST_UNKNOWN_SOURCER}))
        self.assertEqual(str(error.exception),
                         'Source %s has an unknown sourcer' % self.TEST_UNKNOWN_SOURCER,
                         'Wrong error raised')

    def test_sourcer_feedparser(self):
        articles_result = self.articles_actor.ask({'source': self.TEST_SOURCE})
        self.assertIsInstance(articles_result,
                              Iterator,
                              'Iterator expected')
        for article in articles_result:
            self.assertEqual(article['source'],
                             self.TEST_SOURCE,
                             'Returned article has wrong source')
            self.assertIn('id',
                          article,
                          'Article has no id')
            self.assertIn('url',
                          article,
                          'Article has no url')
