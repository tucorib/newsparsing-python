'''
Created on 4 janv. 2018

@author: tuco
'''
import unittest
from newsparsing.sniffer.sourcers.config.rss import get_rss_sources
from newsparsing.sniffer.sniffer import sniff
from newsparsing.sniffer.sourcers import SourceType


class TestSniffer(unittest.TestCase):
    
    def runTest(self):
        self.test_sniff_rss_sources()
        
    def test_sniff_rss_sources(self):
        for rss_source in get_rss_sources():
            sniff(SourceType.RSS, rss_source)