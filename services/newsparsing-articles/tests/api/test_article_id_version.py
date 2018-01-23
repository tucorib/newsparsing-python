'''
Created on 5 janv. 2018

@author: tuco
'''
import time
import unittest

from flask import json
from api import ArticleTestCase


class ArticleIdVersionTestCase(unittest.TestCase, ArticleTestCase):

    def get_api_url(self):
        return '/article/%s/%d' % (self.get_test_id(), 0)

    def get_allowed_methods(self):
        return ['GET']

    def setUp(self):
        ArticleTestCase.setUp(self)

        # Build content
        self.test_content = self.get_test_content()

        # Insert article
        self.client.post('/article',
                         data=json.dumps({
                             'id': self.get_test_id(),
                             'content': self.test_content
                             }),
                         headers={'Content-Type': 'application/json'})

    def test_get(self):
        # Get unexisting version of article
        response = self.client.get('/article/%s/%d' % (self.get_test_id(), 2))
        self.assertResponseCode(response, 404)

        # Get first version of article
        response = self.client.get('/article/%s/%d' % (self.get_test_id(), 0))
        self.assertResponseCode(response, 200)
        self.assertDictEqual(json.loads(response.data), {'_id': {'_id': self.get_test_id(), 'version': 0}, 'content': self.test_content}, 'Test article in DB is not expected: %s' % response.data)

        # Wait
        time.sleep(1)
        test_content_1 = self.get_test_content()

        # Update article with no content
        response = self.client.post('/article',
                                    data=json.dumps({
                                        'id': self.get_test_id(),
                                        'content': test_content_1
                                        }),
                                    headers={'Content-Type': 'application/json'})

        # Get second version of article
        response = self.client.get('/article/%s/%d' % (self.get_test_id(), 1))
        self.assertResponseCode(response, 200)
        self.assertDictEqual(json.loads(response.data), {'_id': {'_id': self.get_test_id(), 'version': 1}, 'content': test_content_1}, 'Test article in DB is not expected: %s' % response.data)
