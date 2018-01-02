'''
Created on 2 janv. 2018

@author: tuco
'''
from pyhocon.config_parser import ConfigFactory
import logging

# Configuration
configuration = None


def load(configuration_path):
    global configuration
    configuration = ConfigFactory.parse_file(configuration_path)
    
    if configuration.get('loggers.articles'):
        logging.config.fromConfig(configuration.get('loggers.articles'))
        logger = logging.getLogger('articles')
        logger.debug('Loaded: %s' % configuration.get('loggers.articles'))


def get_configuration():
    global configuration
    return configuration