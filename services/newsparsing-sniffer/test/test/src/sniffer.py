'''
Created on 5 janv. 2018

@author: tuco
'''
import unittest
from test.src import SnifferTest
from newsparsing.sniffer.sniffer import sniff
from newsparsing.sniffer.sourcers import SourceType


class TestSniffer(unittest.TestCase, SnifferTest):
    
    def setUp(self):
        unittest.TestCase.setUp(self)
        SnifferTest.setUp(self)

    def test_sniffer_rss(self):
        articles = sniff(SourceType.RSS, 'lorem-rss')
        print(articles)
        