'''
Created on 5 janv. 2018

@author: tuco
'''
import unittest
from test.src import SourcersTest
from newsparsing.sourcers.feedparse import get_articles


class TestRss(unittest.TestCase, SourcersTest):
    
    TEST_RSS = 'lorem-rss'
    
    def setUp(self):
        unittest.TestCase.setUp(self)
        SourcersTest.setUp(self)
        
    def test_get_articles(self):
        get_articles(self.TEST_RSS)
