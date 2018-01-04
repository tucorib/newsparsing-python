'''
Created on 2 janv. 2018

@author: tuco
'''
from pymongo.mongo_client import MongoClient
import pymongo
from newsparsing.articles.config.application import get_storage_database_name, \
    get_storage_database_url
from newsparsing.articles.dao import VersionnedDataBuilder


def __get_articles_db():
    client = MongoClient(get_storage_database_url())
    db = client[get_storage_database_name()]
    articles_db = db['articles']
    # Create index
    articles_db.create_index([("_id", pymongo.ASCENDING)], unique=True)
    articles_db.create_index([("_id", pymongo.ASCENDING),
                              ("version", pymongo.DESCENDING)])
    
    return articles_db


def get_article(_id, version=None):
    # Build DAO object
    data_builder = VersionnedDataBuilder(_id)
    # Get versions
    versions = []
    for _ in __get_articles_db().find(data_builder.build_dao_query(version=version)).sort([("version", pymongo.ASCENDING)]):
        versions.append(_)
    # Build article
    return data_builder.build_data_from_versions(versions)


def store_article(_id, content):
    # Builders
    data_builder = VersionnedDataBuilder(_id)
    # Get latest version
    latest_version = get_article(_id)
    # Build new version
    new_version = data_builder.build_data_from_content(content)
    
    # Check if neep to upsert
    if not 'published' in latest_version['content'] or content['published'] > latest_version['content']['published']:
        # Compute diff
        current_diff = data_builder.build_content_diff(latest_version, new_version)
        # Build DAO diff
        dao_diff = data_builder.build_new_dao_version(latest_version, current_diff)
        # Store diff
        __get_articles_db().save(dao_diff)
