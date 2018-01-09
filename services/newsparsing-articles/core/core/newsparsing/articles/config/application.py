'''
Created on 1 janv. 2018

@author: tuco
'''
import logging.config

from pyhocon.config_parser import ConfigFactory

# Configuration
configuration = None

logger = logging.getLogger('newsparsing.articles')


def load_configuration(configuration_path):
    global configuration
    configuration = ConfigFactory.parse_file(configuration_path)

    if configuration.get('logger', None):
        logging.config.fileConfig(configuration['logger'])

    logger.debug('Configuration: %s' % configuration_path)


def get_configuration():
    global configuration
    return configuration


def get_storage_database_url():
    return get_configuration().get('storage.url', None)


def get_storage_database_name():
    return get_configuration().get('storage.name', None)
