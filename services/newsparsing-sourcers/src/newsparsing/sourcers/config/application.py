'''
Created on 4 janv. 2018

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
