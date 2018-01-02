'''
Created on 2 janv. 2018

@author: tuco
'''
from newsparsing.common import VersionnedDataBuilder


class ArticleDataBuilder(VersionnedDataBuilder):
    
    def __init__(self, source_type, source_name, _id):
        self._id = {
            '_id': _id,
            'source': {
                'name': source_name,
                'type': source_type
            }
        }
