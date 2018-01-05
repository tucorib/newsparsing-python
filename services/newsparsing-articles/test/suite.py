'''
Created on 4 janv. 2018

@author: tuco
'''
import unittest
import sys
from test.newsparsing.articles.config.application import TestConfiguration
from test.newsparsing.articles.test_storage import TestStorage
from test.newsparsing.articles.dao.articles import TestArticles

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
    # Tests
    suite.addTest(TestStorage())
    suite.addTest(TestArticles())
    # Run tests
    runner.run(suite)
