'''
Created on 4 janv. 2018

@author: tuco
'''
from dictdiffer import patch, diff


def get_data(collection, _id, version=None):
    # Get versions
    versions = []
    # Build filter
    _filter = {'_id._id': _id}
    if not version is None:
        _filter['_id.version'] = {'$lte': version}

    for _ in collection.find(_filter).sort([('_id.version', 1)]):
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

    # Return version
    return new_version


def delete_data(collection, _id, version=None):
    _filter = {'_id._id': _id}
    if version:
        _filter['_id.version': version]

    # Delete data
    collection.delete_many(_filter)
