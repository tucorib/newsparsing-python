'''
Created on 4 janv. 2018

@author: tuco
'''
import logging.config

from pyhocon.config_parser import ConfigFactory

# Configuration
configuration = None

logger = logging.getLogger('newsparsing.sniffer')


def load_configuration(configuration_path):
    global configuration
    configuration = ConfigFactory.parse_file(configuration_path)

    if configuration.get('logger', None):
        logging.config.fileConfig(configuration['logger'])

    logger.debug('Configuration: %s' % configuration_path)


def get_configuration():
    global configuration
    return configuration


def get_service_sourcers():
    return get_configuration().get('services.sourcers', None)


def get_service_extractors():
    return get_configuration().get('services.extractors', None)


def get_service_articles():
    return get_configuration().get('services.articles', None)


def get_sourcetypes():
    return get_configuration().get('sources', {}).keys()


def get_sources(source_type):
    return get_configuration().get('sources.%s' % source_type, {}).keys()


def get_source_fields(source_type, source):
    return get_configuration().get('sources.%s.%s.fields' % (source_type, source), {}).keys()


def get_source_field_extractors(source_type, source, field):
    return get_configuration().get('sources.%s.%s.fields.%s.extractors' % (source_type, source, field), [])
