'''
Created on 1 janv. 2018

@author: tuco
'''
from newsparsing.common.configuration import get_configuration


def get_storage_database_url():
    return get_configuration().get('storage.url', None)


def get_storage_database_name():
    return get_configuration().get('storage.name', None)
