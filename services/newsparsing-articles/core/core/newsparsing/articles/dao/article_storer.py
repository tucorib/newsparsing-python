'''
Created on 11 janv. 2018

@author: nribeiro
'''
from dictdiffer import diff
import pykka
from pymongo.mongo_client import MongoClient

from core.newsparsing.articles.config.application import get_storage_database_url, \
    get_storage_database_name
from core.newsparsing.articles.dao.article_getter import ArticleGetterActor


class ArticleStorerActor(pykka.ThreadingActor):

    def __get_articles_db(self):
        client = MongoClient(get_storage_database_url())
        db = client[get_storage_database_name()]
        articles_db = db['articles']
        return articles_db

    def on_receive(self, message):
        _id = message['id']
        content = message['content']

        # Get latest version
        article_getter_actor = ArticleGetterActor.start()
        last_version = article_getter_actor.ask({'id': _id})
        # Stop actor
        article_getter_actor.stop()

        # Get current version
        version = None
        if last_version is not None:
            version = last_version['_id'].get('version', None)

        # Build new version
        new_version = {
            '_id': {
                '_id': _id,
                'version': version
            },
            'content': content
        }

        # Check if neep to upsert
        if last_version is None or new_version['content']['published'] > last_version['content']['published']:
            # Store data
            data_id = new_version['_id']['_id']

            assert last_version is None or not diff(last_version['_id']['_id'], data_id) == {}, "Data don't have same ids"

            # Compute diff and new version
            if last_version is None:
                current_diff = diff({}, new_version['content'])
                version = 0
            else:
                current_diff = diff(last_version['content'], new_version['content'])
                version = last_version['_id']['version'] + 1

            # Build DAO diff
            dao_diff = {
                '_id': {
                    '_id': data_id,
                    'version': version
                },
                'diff': list(current_diff)
            }
            # Store diff
            self.__get_articles_db().save(dao_diff)

        # Return version
        return version
