'''
Created on 2 janv. 2018

@author: tuco
'''
from pymongo.mongo_client import MongoClient
from newsparsing.articles.config.application import get_storage_database_url, \
    get_storage_database_name
import pymongo


def __get_sources_db():
    # Store source
    client = MongoClient(get_storage_database_url())
    db = client[get_storage_database_name()]
    source_db = db['sources']
    # Create index
    source_db.create_index([("name", pymongo.ASCENDING)], unique=True)
    
    return source_db


def store_source(source_type, source_name):
    # Store source
    source_db = __get_sources_db()
    source_db.save({'type': source_type, 'name': source_name})
