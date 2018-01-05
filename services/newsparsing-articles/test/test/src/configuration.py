'''
Created on 5 janv. 2018

@author: tuco
'''
import unittest
import os
from newsparsing.articles.config.application import load
from pyhocon.config_parser import ConfigException


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
        try:
            # Load configuration
            load(self.configuration_filename)
        except ConfigException as err:
            self.fail(err)