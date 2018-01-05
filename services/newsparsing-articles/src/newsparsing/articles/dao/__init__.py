'''
Created on 4 janv. 2018

@author: tuco
'''
from dictdiffer import patch, diff


def get_data(collection, _id, version=None):
    # Build filter
    _filter = {'_id._id': _id}
    if not version is None:
        _filter['_id.version'] = {'$lte': version}
    
    # Get versions
    versions = []
    
    for _ in collection.find(_filter).sort([('_id.version', 1)]):
        versions.append(_)
    
    if len(versions) > 0:
        # Build article
        data = {
            '_id': {
                '_id': _id,
                'version': None
            },
            'content': {}
        }
        if len(versions) > 0:
            data['_id']['version'] = versions[-1]['_id']['version']
        # Set content
        for version in versions:
            patch(version['diff'], data['content'], in_place=True)
        
        return data
    else:
        return None


def build_data(_id, content):
    return {
        '_id': {
            '_id': _id,
            'version': None
        },
        'content': content
    }


def save_data(collection, last_version, data):
    # Get data id
    data_id = data['_id']['_id']
    
    assert last_version is None or not diff(last_version['_id']['_id'], data_id) == {}, "Data don't have same ids"
    
    # Compute diff and new version
    if last_version is None:
        current_diff = diff({}, data['content'])
        new_version = 0
    else:
        current_diff = diff(last_version['content'], data['content'])
        new_version = last_version['_id']['version'] + 1 
    
    # Build DAO diff
    dao_diff = {
        '_id': {
            '_id': data_id,
            'version': new_version
        },
        'diff': list(current_diff)
    }
    # Store diff
    collection.save(dao_diff)

    
def delete_data(collection, _id, version=None):
    _filter = {'_id._id': _id}
    if version:
        _filter['_id.version': version]
    
    # Delete data
    collection.delete_many(_filter)

