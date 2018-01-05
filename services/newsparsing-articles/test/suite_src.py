'''
Created on 4 janv. 2018

@author: tuco
'''
import unittest
import sys
from newsparsing.articles.config.application import load
from test.src.configuration import TestConfiguration
from test.src.storage import TestStorage
from test.src.articles import TestArticles

if __name__ == '__main__':
    # Check configuration argument
    if len(sys.argv) < 2:
        sys.stderr.write('Configuration argument is not passed')
        exit(-1)
    
    # Get configuration path
    configuration = sys.argv[1]
    # Init test suite
    runner = unittest.TextTestRunner()
    suite = unittest.TestSuite()
    
    # Check and init configuration access
    suite.addTest(TestConfiguration(configuration))
    
    # Load configuration
    load(configuration)
            
    # Tests core
    suite.addTest(TestStorage())
    suite.addTest(TestArticles())
    
    # Run tests
    runner.run(suite)
