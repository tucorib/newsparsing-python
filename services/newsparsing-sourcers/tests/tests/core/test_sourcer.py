'''
Created on 9 janv. 2018

@author: nribeiro
'''
import unittest

from core.newsparsing.sourcers.articles import ArticlesActor
from tests.core import SourcersTestCase


class FeedParserTestCase(unittest.TestCase, SourcersTestCase):

    TEST_SOURCE = 'slate'

    def setUp(self):
        unittest.TestCase.setUp(self)
        SourcersTestCase.setUp(self)

    def test_get_articles(self):
        # Start actor
        articles_actor = ArticlesActor.start()
        articles_iterator = articles_actor.ask({'source': self.TEST_SOURCE})
        # Stop actor
        articles_actor.stop()

        for article in articles_iterator:
            self.assertEqual(article['source'], self.TEST_SOURCE, 'Returned article has wrong source')
            self.assertIn('id', article, 'Article has no id')
            self.assertIn('url', article, 'Article has no url')
