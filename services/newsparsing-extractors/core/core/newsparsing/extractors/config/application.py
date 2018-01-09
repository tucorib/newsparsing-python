'''
Created on 6 janv. 2018

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


def get_extractors():
    return get_configuration().get('extractors', [])


def get_extractors_fields(extractor):
    return get_configuration().get('extractors.%s.fields' % extractor, [])
