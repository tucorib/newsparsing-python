'''
Created on 28 dec. 2017

@author: tuco
'''
import unittest
import os
from newsparsing.articles.config.application import load


class TestConfiguration(unittest.TestCase):
    
    def __init__(self, configuration_filename, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)
        self.configuration_filename = configuration_filename
    
    def runTest(self):
        self.test_load_configuration()
        
    def test_load_configuration(self):
        # Configuration filename not empty
        self.assertNotIn(self.configuration_filename, [None, ""], 'Configuration filename is empty')
        # Filename exists
        self.assertTrue(os.path.exists(self.configuration_filename), 'Configuration file does not exist')
        # Load configuration
        load(self.configuration_filename)
        
