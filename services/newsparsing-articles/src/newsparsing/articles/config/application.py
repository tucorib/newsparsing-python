'''
Created on 1 janv. 2018

@author: tuco
'''
from pyhocon.config_parser import ConfigFactory
import logging.config

# Configuration
configuration = None


def load(configuration_path):
    global configuration
    configuration = ConfigFactory.parse_file(configuration_path)
    
    if configuration.get('logger', None):
        logging.config.fileConfig(configuration['logger'])


def get_configuration():
    global configuration
    return configuration


def get_storage_database_url():
    return get_configuration().get('storage.url', None)


def get_storage_database_name():
    return get_configuration().get('storage.name', None)
