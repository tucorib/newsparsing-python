'''
Created on 4 janv. 2018

@author: tuco
'''
import unittest
from newsparsing.articles.config.application import get_storage_database_name, get_storage_database_url
from pymongo.errors import ServerSelectionTimeoutError
from pymongo.mongo_client import MongoClient


class TestStorage(unittest.TestCase):
    
    def runTest(self):
        self.test_storage_url()
        self.test_storage_name()
    
    def __getMongoClient(self):
        client = MongoClient(get_storage_database_url(),
                             serverSelectionTimeoutMS=5000)
        client.server_info()
        
        return client
        
    def test_storage_url(self):
        try:
            # Connect to mongodb
            self.__getMongoClient()
        except ServerSelectionTimeoutError as err:
            self.fail(err)
    
    def test_storage_name(self):
        try:
            # Connect to mongodb
            client = self.__getMongoClient()
             
            self.assertTrue(get_storage_database_name() in client.database_names(), '%s not in server %s' % (get_storage_database_name(),
                                                                                                             get_storage_database_url()))
        except ServerSelectionTimeoutError as err:
            self.fail(err)
