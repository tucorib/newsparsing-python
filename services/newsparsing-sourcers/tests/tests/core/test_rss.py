'''
Created on 5 janv. 2018

@author: tuco
'''
import unittest

from core.newsparsing.sourcers.core import SourceType
from core.newsparsing.sourcers.core.source import get_articles
from tests.core import SourcersTestCase


class RsstestCase(unittest.TestCase, SourcersTestCase):
    
    TEST_RSS = 'slate'
    
    def setUp(self):
        unittest.TestCase.setUp(self)
        SourcersTestCase.setUp(self)
        
    def test_get_articles(self):
        get_articles(SourceType.RSS, self.TEST_RSS)
