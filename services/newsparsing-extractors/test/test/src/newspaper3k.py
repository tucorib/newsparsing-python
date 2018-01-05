'''
Created on 5 janv. 2018

@author: tuco
'''
import unittest
from test.src import TestExtractor


class TestNewspaper3k(unittest.TestCase, TestExtractor):
    
    def get_test_url(self):
        return "http://edition.cnn.com/2013/11/27/justice/tucson-arizona-captive-girls/"
    
    def get_expected_fields(self):
        return ['title', 'text', 'authors']
    
