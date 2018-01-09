'''
Created on 5 janv. 2018

@author: tuco
'''
import datetime
import json
import time
import unittest

from tests.api import ArticleTestCase


class TestArticle(unittest.TestCase, ArticleTestCase):

    def get_api_url(self):
        return '/article'

    def get_allowed_methods(self):
        return ['POST']

    def get_test_id(self):
        return 'test'

    def get_test_content(self):
        return {'published': datetime.datetime.utcnow().replace(microsecond=0).timestamp()}

    def setUp(self):
        ArticleTestCase.setUp(self)

    def test_post(self):
        # Empty
        response = self.client.post('/article',
                                    data=json.dumps({}),
                                    headers={'Content-Type': 'application/json'})
        self.assertResponseCode(response, 403)

        # No id
        response = self.client.post('/article',
                                    data=json.dumps({
                                        'content': self.get_test_content()
                                        }),
                                    headers={'Content-Type': 'application/json'})
        self.assertResponseCode(response, 403)

        # No content
        response = self.client.post('/article',
                                    data=json.dumps({
                                        'id': self.get_test_id(),
                                        }),
                                    headers={'Content-Type': 'application/json'})
        self.assertResponseCode(response, 403)

        # Full
        response = self.client.post('/article',
                                    data=json.dumps({
                                        'id': self.get_test_id(),
                                        'content': self.get_test_content()
                                        }),
                                    headers={'Content-Type': 'application/json'})
        self.assertResponseCode(response, 201)

        # Wait
        time.sleep(1)

        # Update article
        response = self.client.post('/article',
                                    data=json.dumps({
                                        'id': self.get_test_id(),
                                        'content': self.get_test_content()
                                        }),
                                    headers={'Content-Type': 'application/json'})
        self.assertResponseCode(response, 200)
