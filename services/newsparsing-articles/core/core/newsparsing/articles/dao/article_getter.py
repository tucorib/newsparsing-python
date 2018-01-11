'''
Created on 11 janv. 2018

@author: nribeiro
'''
from dictdiffer import patch
import pykka
from pymongo.mongo_client import MongoClient

from core.newsparsing.articles.config.application import get_storage_database_url, \
    get_storage_database_name


class ArticleGetterActor(pykka.ThreadingActor):

    def __get_articles_db(self):
        client = MongoClient(get_storage_database_url())
        db = client[get_storage_database_name()]
        articles_db = db['articles']
        return articles_db

    def on_receive(self, message):
        _id = message['id']
        version = message.get('version', None)

        # Get versions
        versions = []
        # Build filter
        _filter = {'_id._id': _id}
        if not version is None:
            _filter['_id.version'] = {'$lte': version}

        for _ in self.__get_articles_db().find(_filter).sort([('_id.version', 1)]):
            versions.append(_)

        # Build article
        data = {
            '_id': {
                '_id': _id,
                'version': None
            },
            'content': {}
        }

        if len(versions) > 0:
            # Build article if no version specified or if last version is version
            if version is None or versions[-1]['_id']['version'] == version:
                data['_id']['version'] = versions[-1]['_id']['version']

                # Set content
                for version in versions:
                    patch(version['diff'], data['content'], in_place=True)

                return data

        return None
