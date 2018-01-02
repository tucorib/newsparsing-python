'''
Created on 28 dec. 2017

@author: tuco
'''
import unittest
from test.newsparsing.articles.sources import TestSources
import sys
from test.newsparsing.articles.sniffers.rss import TestSnifferRss
from test.newsparsing.articles.config.application import TestConfiguration

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
    suite.addTest(TestSources())
    suite.addTest(TestSnifferRss())
    # Run tests
    runner.run (suite)
