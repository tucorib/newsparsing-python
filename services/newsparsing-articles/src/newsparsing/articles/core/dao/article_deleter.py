'''
Created on 11 janv. 2018

@author: nribeiro
'''
import pykka
from pymongo.mongo_client import MongoClient
from newsparsing.articles.core.config.application import get_storage_database_url, \
    get_storage_database_name


class ArticleDeleterActor(pykka.ThreadingActor):

    def __get_articles_db(self):
        client = MongoClient(get_storage_database_url())
        db = client[get_storage_database_name()]
        articles_db = db['articles']
        return articles_db

    def on_receive(self, message):
        _id = message['id']
        version = message.get('version', None)

        _filter = {'_id._id': _id}
        if version:
            _filter['_id.version': version]

        # Delete data
        self.__get_articles_db().delete_many(_filter)
