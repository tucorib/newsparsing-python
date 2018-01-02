'''
Created on 1 janv. 2018

@author: tuco
'''
from newsparsing.sourcers.config.rss import get_rss_sources
import unittest
from newsparsing.articles.sniffer import sniff


class TestSnifferRss(unittest.TestCase):
    
    def runTest(self):
        self.test_sniff_rss_source()
        
    def test_sniff_rss_source(self):
        for rss_source in get_rss_sources():
            sniff('rss', rss_source)
            
