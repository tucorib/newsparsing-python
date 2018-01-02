'''
Created on 2 janv. 2018

@author: tuco
'''
from pymongo.mongo_client import MongoClient
import pymongo
import logging
from newsparsing.sourcers import get_source_database_url, \
    get_source_database_name
from newsparsing.common.models.articles import ArticleDataBuilder


def __get_articles_db(rss_source_name):
    client = MongoClient(get_source_database_url(rss_source_name))
    db = client[get_source_database_name(rss_source_name)]
    articles_db = db['articles']
    # Create index
    articles_db.create_index([("_id", pymongo.ASCENDING)], unique=True)
    articles_db.create_index([("_id", pymongo.ASCENDING),
                              ("version", pymongo.DESCENDING)])
    
    return articles_db


def get_article(source_name, dao_id, version=None):
    # Build DAO object
    data_builder = ArticleDataBuilder(dao_id)
    # Get versions
    versions = []
    for _ in __get_articles_db(source_name).find(data_builder.build_dao_query(version=version)).sort([("version", pymongo.ASCENDING)]):
        versions.append(_)
    # Build article
    return data_builder.build_data_from_versions(versions)


def store_article(source_name, article):
    logger = logging.getLogger('articles')
    # Builders
    dao_id = article['_id']
    data_builder = ArticleDataBuilder(dao_id)
    # Get latest version
    latest_version = get_article(source_name, dao_id)
    
    # Check if neep to upsert
    if not 'published' in latest_version['content'] or article['content']['published'] > latest_version['content']['published']:
        # Compute diff
        current_diff = data_builder.build_content_diff(latest_version, article)
        # Build DAO diff
        dao_diff = data_builder.build_new_dao_version(article, current_diff)
        # Store diff
        __get_articles_db(source_name).save(dao_diff)
        logger.debug('[%s] Article %s stored' % (source_name, dao_id))
        print('[%s] Article %s stored' % (source_name, dao_id))
