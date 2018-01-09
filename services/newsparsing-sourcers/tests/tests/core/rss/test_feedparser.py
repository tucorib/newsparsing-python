'''
Created on 9 janv. 2018

@author: nribeiro
'''
import unittest

from core.newsparsing.sourcers.rss.feedparser import get_feedparser_articles
from tests.core import SourcersTestCase


class FeedParserTestCase(unittest.TestCase, SourcersTestCase):

    TEST_SOURCER = 'slate'

    def setUp(self):
        unittest.TestCase.setUp(self)
        SourcersTestCase.setUp(self)

    def test_get_articles(self):
        get_feedparser_articles(self.TEST_SOURCER)
