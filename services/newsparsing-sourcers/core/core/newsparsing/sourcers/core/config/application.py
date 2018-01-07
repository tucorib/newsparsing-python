'''
Created on 4 janv. 2018

@author: tuco
'''
import logging.config

from pyhocon.config_parser import ConfigFactory

# Configuration
configuration = None


def load_configuration(configuration_path):
    global configuration
    configuration = ConfigFactory.parse_file(configuration_path)
    
    if configuration.get('logger', None):
        logging.config.fileConfig(configuration['logger'])

    
def get_configuration():
    global configuration
    return configuration
