'''
Created on 4 janv. 2018

@author: tuco
'''
import datetime
import time
import unittest

from core.newsparsing.articles.dao.articles import store_article, \
    get_article, delete_article
from tests.core import ArticlesTestCase


class TestArticles(unittest.TestCase, ArticlesTestCase):

    def __get_test_id(self):
        return 'tests'

    def __get_test_content(self):
        return {'published': datetime.datetime.utcnow().replace(microsecond=0).timestamp()}

    def setUp(self):
        unittest.TestCase.setUp(self)
        ArticlesTestCase.setUp(self)
        # Clear tests document
        delete_article(self.__get_test_id())

    def test_save(self):
        # Insert
        version = store_article(self.__get_test_id(), self.__get_test_content())

        self.assertEqual(version, 0, 'Wrong version')

    def test_query(self):
        # Document content
        content = self.__get_test_content()
        # Insert
        store_article(self.__get_test_id(), content)
        # Get article
        article = get_article(self.__get_test_id())

        self.assertDictEqual(article, {'_id': {'_id': self.__get_test_id(), 'version': 0}, 'content': content}, 'Test article in DB is not expected: %s' % article)

    def test_same_version_save(self):
        # Document content
        content = self.__get_test_content()
        # Insert
        store_article(self.__get_test_id(), content)
        # Re-insert same document
        version_1 = store_article(self.__get_test_id(), content)

        self.assertIsNone(version_1, 'Wrong version')

        # Get article
        article = get_article(self.__get_test_id())

        self.assertEqual(article, {'_id': {'_id': self.__get_test_id(), 'version': 0}, 'content': content}, 'Test article in DB is not expected: %s' % article)

    def test_different_version_save(self):
        # Insert
        store_article(self.__get_test_id(), self.__get_test_content())
        # Wait for new published date
        time.sleep(1)
        # Re-insert not same document
        version_1 = store_article(self.__get_test_id(), self.__get_test_content())

        self.assertEqual(version_1, 1, 'Wrong version')

        # Get article
        article = get_article(self.__get_test_id())

        self.assertEqual(article['_id']['version'], 1, 'Test article in DB is not expected: %s' % article)

    def test_select_old_version_query(self):
        # Document content
        content = self.__get_test_content()
        # Insert
        store_article(self.__get_test_id(), content)
        # Wait for new published date
        time.sleep(1)
        # Re-insert not same document
        store_article(self.__get_test_id(), self.__get_test_content())

        # Get old article
        article = get_article(self.__get_test_id(), version=0)

        self.assertEqual(article, {'_id': {'_id': self.__get_test_id(), 'version': 0}, 'content': content}, 'Test article in DB is not expected: %s' % article)
