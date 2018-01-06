'''
Created on 5 janv. 2018

@author: tuco
'''
import unittest
from test.src import SourcersTest
from newsparsing.sourcers.source import get_articles
from newsparsing.sourcers import SourceType


class TestRss(unittest.TestCase, SourcersTest):
    
    TEST_RSS = 'lorem-rss'
    
    def setUp(self):
        unittest.TestCase.setUp(self)
        SourcersTest.setUp(self)
        
    def test_get_articles(self):
        get_articles(SourceType.RSS, self.TEST_RSS)
