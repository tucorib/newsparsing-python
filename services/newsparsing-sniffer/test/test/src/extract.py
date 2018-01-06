'''
Created on 6 janv. 2018

@author: tuco
'''
import unittest
from test import SnifferTest
from newsparsing.sniffer.sniffer import sniff


class TestSniffer(unittest.TestCase, SnifferTest):
    
    def setUp(self):
        unittest.TestCase.setUp(self)
        SnifferTest.setUp(self)

    def test_sniff(self):
        # Sniff RSS
        sniff('rss', 'lorem-rss')
