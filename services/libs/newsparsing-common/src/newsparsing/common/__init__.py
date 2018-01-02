'''
Created on 2 janv. 2018

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
        return {'_id': self._id}
        
    def build_data_from_content(self, content, version=None):
        return {
            '_id': self._id,
            'version': version,
            'content': content
        }
        
    def build_data_from_versions(self, versions):
        data = {
            '_id': self._id,
            'version': None,
            'content': {}
        }
        # Set version
        if len(versions) > 0:
            data['version'] = versions[-1]['version']
        # Set content
        for version in versions:
            patch(version['diff'], data['content'])
        
        return data

    def build_content_diff(self, old_data, new_data):
        assert not diff(old_data['_id'], new_data['_id']) == {}, "Data don't have same ids"
        
        return diff(old_data['content'], new_data['content'])
    
    def build_new_dao_version(self, last_version, new_diff):
        new_version = 0
        if last_version['version']:
            new_version = last_version['version'] + 1 
        return {
            '_id': self._id,
            'version': new_version,
            'diff': list(new_diff)
        }
    
    def build_dao_query(self, version=None):
        query = self.dao_id
        if query is not None:
            query = {**query, **{'version': {'$lte': version}}}
        return query
    
