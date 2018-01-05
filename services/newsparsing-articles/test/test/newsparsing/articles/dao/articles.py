'''
Created on 4 janv. 2018

@author: tuco
'''
import unittest
from newsparsing.articles.dao.articles import get_articles_db, store_article, \
    get_article
from newsparsing.articles.dao import VersionnedDataBuilder
import datetime
import time


class TestArticles(unittest.TestCase):
    
    def runTest(self):
        self.test_save()
        self.__clear_db()
        self.test_query()
        self.__clear_db()
        self.test_same_version_save()
        self.__clear_db()
        self.test_different_version_save()
        self.__clear_db()
        self.test_select_old_version_query()
    
    def __get_test_id(self):
        return 'test'
    
    def __get_test_content(self):
        return {'published': datetime.datetime.utcnow().replace(microsecond=0)}
    
    def __clear_db(self):
        # Get mongodb
        self.db = get_articles_db()
        # Get data builder
        self.data_builder = VersionnedDataBuilder(self.__get_test_id())
        # Clear test document
        self.db.delete_many({'_id._id': self.__get_test_id()})
        
    def setUp(self):
        self.__clear_db()

    def test_save(self):
        # Insert
        store_article(self.__get_test_id(), self.__get_test_content())
    
    def test_query(self):
        # Document content
        content = self.__get_test_content()
        # Insert
        store_article(self.__get_test_id(), content)
        # Get mongodb document
        mongo_document = get_article(self.__get_test_id())
        
        self.assertDictEqual(mongo_document, {'_id': {'_id': self.__get_test_id(), 'version': 0}, 'content': content}, 'Test article in DB is not expected: %s' % mongo_document)
            
    def test_same_version_save(self):
        # Document content
        content = self.__get_test_content()
        # Insert
        store_article(self.__get_test_id(), content)
        # Re-insert same document
        store_article(self.__get_test_id(), content)
        
        # Get mongodb document
        mongo_document = get_article(self.__get_test_id())
        
        self.assertEqual(mongo_document, {'_id': {'_id': self.__get_test_id(), 'version': 0}, 'content': content}, 'Test article in DB is not expected: %s' % mongo_document)

    def test_different_version_save(self):
        # Insert
        store_article(self.__get_test_id(), self.__get_test_content())
        # Wait for new published date
        time.sleep(1)
        # Re-insert not same document
        store_article(self.__get_test_id(), self.__get_test_content())
        
        # Get mongodb document
        mongo_document = get_article(self.__get_test_id())
        
        self.assertEqual(mongo_document['_id']['version'], 1, 'Test article in DB is not expected: %s' % mongo_document)
            
    def test_select_old_version_query(self):
        # Document content
        content = self.__get_test_content()
        # Insert
        store_article(self.__get_test_id(), content)
        # Wait for new published date
        time.sleep(1)
        # Re-insert not same document
        store_article(self.__get_test_id(), self.__get_test_content())
        
        # Get old mongodb document
        mongo_document = get_article(self.__get_test_id(), version=0)
        
        self.assertEqual(mongo_document, {'_id': {'_id': self.__get_test_id(), 'version': 0}, 'content': content}, 'Test article in DB is not expected: %s' % mongo_document)
            
