'''
Created on 2 janv. 2018

@author: tuco
'''
from pymongo.mongo_client import MongoClient
from newsparsing.articles.config.application import get_storage_database_name, \
    get_storage_database_url
from newsparsing.articles.dao import  \
    build_data, get_data, save_data, delete_data


def get_articles_db():
    client = MongoClient(get_storage_database_url())
    db = client[get_storage_database_name()]
    articles_db = db['articles']
    return articles_db


def get_article(_id, version=None):
    return get_data(get_articles_db(), _id, version)


def store_article(_id, content):
    # Get latest version
    last_version = get_article(_id)
    # Build new version
    new_version = build_data(_id, content)
    
    # Check if neep to upsert
    if last_version is None or new_version['content']['published'] > last_version['content']['published']:
        # Store data
        return save_data(get_articles_db(), last_version, new_version)
    

def delete_article(_id):
    delete_data(get_articles_db(), _id, version=None)
    
