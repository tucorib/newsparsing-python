'''
Created on 4 janv. 2018

@author: tuco
'''
from dictdiffer import patch, diff

            
class VersionnedDataBuilder(object):
    
    def __init__(self, _id):
        self._id = _id
    
    @property
    def id(self):
        return self._id
    
    @property
    def dao_id(self):
        return {'_id': {'_id': self._id}}
        
    def build_data_from_content(self, content, version=None):
        return {
            '_id': {
                '_id': self._id,
                'version': version
            },
            'content': content
        }
        
    def build_data_from_versions(self, versions):
        data = {
            '_id': {
                '_id': self._id,
                'version': None
            },
            'content': {}
        }
        # Set version
        if len(versions) > 0:
            data['_id']['version'] = versions[-1]['_id']['version']
        # Set content
        for version in versions:
            patch(version['diff'], data['content'], in_place=True)
        
        return data

    def build_content_diff(self, old_data, new_data):
        assert not diff(old_data['_id']['_id'], new_data['_id']['_id']) == {}, "Data don't have same ids"
        
        return diff(old_data['content'], new_data['content'])
    
    def build_new_dao_version(self, last_version, new_diff):
        new_version = 0
        if not last_version['_id']['version'] is None:
            new_version = last_version['_id']['version'] + 1 
        return {
            '_id': {
                '_id': self._id,
                'version': new_version
            },
            'diff': list(new_diff)
        }
    
