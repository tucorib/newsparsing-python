'''
Created on 5 janv. 2018

@author: tuco
'''
import datetime
import unittest

from flask import json

from tests.api import ArticleTestCase


class TestArticleId(unittest.TestCase, ArticleTestCase):

    def get_api_url(self):
        return '/article/%s' % self.get_test_id()

    def get_allowed_methods(self):
        return ['GET', 'DELETE']

    def get_test_id(self):
        return 'test'

    def get_test_content(self):
        return {'published': datetime.datetime.utcnow().replace(microsecond=0).timestamp()}

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
        # Unexisting id
        response = self.client.get('/article/%s' % 'error')
        self.assertResponseCode(response, 404)

        # Get article
        response = self.client.get('/article/%s' % self.get_test_id())
        self.assertResponseCode(response, 200)
        self.assertDictEqual(json.loads(response.data), {'_id': {'_id': self.get_test_id(), 'version': 0}, 'content': self.test_content}, 'Test article in DB is not expected: %s' % response.data)

    def test_delete(self):
        # Delete article
        response = self.client.delete('/article/%s' % self.get_test_id(),
                                      data=json.dumps({
                                          'id': self.get_test_id(),
                                          'content': self.get_test_content()
                                          }),
                                      headers={'Content-Type': 'application/json'})
        self.assertResponseCode(response, 204)

