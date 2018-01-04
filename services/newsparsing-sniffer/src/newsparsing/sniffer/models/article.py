'''
Created on 4 janv. 2018

@author: tuco
'''
import json


class Article(object):
    
    def __init__(self, source_type, source_name, _id):
        # Id
        self._id = {
            'source': {
                'type': source_type,
                'name': source_name
            },
            'id': _id
        }
        # Init content
        self.content = {}
    
    def set_content(self, name, value):
        self.content[name] = value
    
    def get_content(self, name):
        return self.content.get(name, None)
    
    def json(self):
        return json.dumps({
            'id': self._id,
            'content': self.content
        })
