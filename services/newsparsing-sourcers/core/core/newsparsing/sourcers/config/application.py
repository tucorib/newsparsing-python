'''
Created on 4 janv. 2018

@author: tuco
'''
import logging.config

from pyhocon.config_parser import ConfigFactory

# Configuration
configuration = None

logger = logging.getLogger('newsparsing.sourcers')


def load_configuration(configuration_path):
    global configuration
    configuration = ConfigFactory.parse_file(configuration_path)

    if configuration.get('logger', None):
        logging.config.fileConfig(configuration['logger'])

    logger.debug('Configuration: %s' % configuration_path)


def get_configuration():
    global configuration
    return configuration


def get_sources():
    return list(get_configuration().get('sources').keys())


def get_source_database_name(source):
    return get_configuration().get('sources.%s.storage.name' % source,
                                   None)


def get_source_database_url(source):
    return get_configuration().get('sources.%s.storage.url' % source,
                                   None)


def get_source_sourcer(source):
    return get_configuration().get('sources.%s.sourcer' % source,
                                   None)

