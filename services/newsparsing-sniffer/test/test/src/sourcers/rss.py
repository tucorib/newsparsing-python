'''
Created on 5 janv. 2018

@author: tuco
'''
import unittest
from test.src import SnifferTest
from newsparsing.sniffer.sourcers.config.rss import get_rss_sources, \
    SOURCE_RSS_DEFAULT, get_rss_source_url
import requests


class TestRss(unittest.TestCase, SnifferTest):
    
    def setUp(self):
        unittest.TestCase.setUp(self)
        SnifferTest.setUp(self)
        
    def test_access(self):
        for rss_source in get_rss_sources():
            if not rss_source == SOURCE_RSS_DEFAULT:
                rss_source_url = get_rss_source_url(rss_source)
                # Url is not empty
                self.assertNotIn(rss_source_url, [None, ""], "Rss source '%s' url is empty" % rss_source)
                # Url is available
                url_code = requests.get(rss_source_url).status_code
                self.assertEqual(url_code, 200, "Rss source '%s' not available (code %d)" % (rss_source,
                                                                                             url_code))
