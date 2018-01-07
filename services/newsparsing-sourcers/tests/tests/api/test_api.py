'''
Created on 7 janv. 2018

@author: tuco
'''
import unittest
from tests.api import FlaskTestCase


class APITestCase(unittest.TestCase, FlaskTestCase):
    
    WRONG_URL = '/wrong/url'
    
    def setUp(self):
        unittest.TestCase.setUp(self)
        FlaskTestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)
        FlaskTestCase.tearDown(self)
        
    def test_404(self):
        response = self.client.get(self.WRONG_URL,
                                   headers=self.get_api_headers())
        self.assertResponseCode(response, 404)
