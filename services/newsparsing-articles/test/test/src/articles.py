'''
Created on 4 janv. 2018

@author: tuco
'''
import unittest
from newsparsing.articles.dao.articles import store_article, \
    get_article, delete_article
import datetime
import time
from test import ArticlesTest


class TestArticles(unittest.TestCase, ArticlesTest):
    
    def __get_test_id(self):
        return 'test'
    
    def __get_test_content(self):
        return {'published': datetime.datetime.utcnow().replace(microsecond=0).timestamp()}
    
    def setUp(self):
        unittest.TestCase.setUp(self)
        ArticlesTest.setUp(self)
        # Clear test document
        delete_article(self.__get_test_id())

    def test_save(self):
        # Insert
        store_article(self.__get_test_id(), self.__get_test_content())
    
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
        store_article(self.__get_test_id(), content)
        
        # Get article
        article = get_article(self.__get_test_id())
        
        self.assertEqual(article, {'_id': {'_id': self.__get_test_id(), 'version': 0}, 'content': content}, 'Test article in DB is not expected: %s' % article)

    def test_different_version_save(self):
        # Insert
        store_article(self.__get_test_id(), self.__get_test_content())
        # Wait for new published date
        time.sleep(1)
        # Re-insert not same document
        store_article(self.__get_test_id(), self.__get_test_content())
        
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
            
