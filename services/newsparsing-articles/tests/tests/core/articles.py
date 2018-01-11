'''
Created on 4 janv. 2018

@author: tuco
'''
import datetime
import time
import unittest

from core.newsparsing.articles.dao.article_deleter import ArticleDeleterActor
from core.newsparsing.articles.dao.article_getter import ArticleGetterActor
from core.newsparsing.articles.dao.article_storer import ArticleStorerActor
from tests.core import ArticlesTestCase


class TestArticles(unittest.TestCase, ArticlesTestCase):

    def __get_test_id(self):
        return 'tests'

    def __get_test_content(self):
        return {'published': datetime.datetime.utcnow().replace(microsecond=0).timestamp()}

    def get_article(self, _id, version=None):
        message = {'id': _id}
        if not version is None:
            message['version'] = version

        # Start actor
        article_getter_actor = ArticleGetterActor.start()
        article = article_getter_actor.ask(message)
        # Stop actor
        article_getter_actor.stop()

        return article

    def store_article(self, _id, content):
        # Start actor
        article_storer_actor = ArticleStorerActor.start()
        version = article_storer_actor.ask({'id': _id,
                                            'content': content
                                            })
        # Stop actor
        article_storer_actor.stop()

        return version

    def delete_article(self, _id):
        # Start actor
        article_deleter_actor = ArticleDeleterActor.start()
        article_deleter_actor.ask({'id': _id},
                                  block=False)
        # Stop actor
        article_deleter_actor.stop()

    def setUp(self):
        unittest.TestCase.setUp(self)
        ArticlesTestCase.setUp(self)
        # Clear tests document
        self.delete_article(self.__get_test_id())

    def test_save(self):
        # Insert
        version = self.store_article(self.__get_test_id(), self.__get_test_content())

        self.assertEqual(version, 0, 'Wrong version')

    def test_query(self):
        # Document content
        content = self.__get_test_content()
        # Insert
        self.store_article(self.__get_test_id(), content)
        # Get article
        article = self.get_article(self.__get_test_id())

        self.assertDictEqual(article, {'_id': {'_id': self.__get_test_id(), 'version': 0}, 'content': content}, 'Test article in DB is not expected: %s' % article)

    def test_store(self):
        # Document content
        content = self.__get_test_content()
        # Insert
        version_0 = self.store_article(self.__get_test_id(), content)
        self.assertEqual(version_0, 0, 'Wrong version')

        # Re-insert same document
        version_1 = self.store_article(self.__get_test_id(), content)
        self.assertEqual(version_1, 0, 'Wrong version')

        # Get article
        article = self.get_article(self.__get_test_id())
        self.assertEqual(article, {'_id': {'_id': self.__get_test_id(), 'version': 0}, 'content': content}, 'Test article in DB is not expected: %s' % article)

        # Wait for new published date
        time.sleep(1)
        # Re-insert not same document
        content = self.__get_test_content()
        version_1 = self.store_article(self.__get_test_id(), self.__get_test_content())
        self.assertEqual(version_1, 1, 'Wrong version')

        # Get article
        article = self.get_article(self.__get_test_id())
        self.assertEqual(article, {'_id': {'_id': self.__get_test_id(), 'version': 1}, 'content': content}, 'Test article in DB is not expected: %s' % article)

    def test_select_old_version_query(self):
        # Document content
        content = self.__get_test_content()
        # Insert
        self.store_article(self.__get_test_id(), content)
        # Wait for new published date
        time.sleep(1)
        # Re-insert not same document
        self.store_article(self.__get_test_id(), self.__get_test_content())

        # Get old article
        article = self.get_article(self.__get_test_id(), version=0)

        self.assertEqual(article, {'_id': {'_id': self.__get_test_id(), 'version': 0}, 'content': content}, 'Test article in DB is not expected: %s' % article)
