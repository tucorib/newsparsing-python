'''
Created on 9 janv. 2018

@author: nribeiro
'''
import unittest

from core.newsparsing.sourcers.sourcer import get_articles
from tests.core import SourcersTestCase


class FeedParserTestCase(unittest.TestCase, SourcersTestCase):

    TEST_SOURCE = 'slate'

    def setUp(self):
        unittest.TestCase.setUp(self)
        SourcersTestCase.setUp(self)

    def test_get_articles(self):
        for article in get_articles(self.TEST_SOURCE):
            self.assertEqual(article['source'], self.TEST_SOURCE, 'Returned article has wrong source')
            self.assertIn('id', article, 'Article has no id')
            self.assertIn('url', article, 'Article has no url')
