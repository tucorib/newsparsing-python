'''
Created on 4 janv. 2018

@author: tuco
'''
import unittest
import sys
from newsparsing.articles.config.application import load
from test.src.configuration import TestConfiguration
from test.api import articles

if __name__ == '__main__':
    # Check configuration argument
    if len(sys.argv) < 3:
        sys.stderr.write('Configuration argument is not passed')
        exit(-1)
    
    # Get articles configuration path
    articles_configuration = sys.argv[1]
    # Get flask configuration path
    flask_configuration = sys.argv[2]
    
    # Init test suite
    runner = unittest.TextTestRunner()
    suite = unittest.TestSuite()
    
    # Check and init configuration access
    suite.addTest(TestConfiguration(articles_configuration))
    
    # Load configuration
    load(articles_configuration)
            
    # Test api
    suite.addTests(articles.suite(flask_configuration))
    
    # Run tests
    runner.run(suite)
