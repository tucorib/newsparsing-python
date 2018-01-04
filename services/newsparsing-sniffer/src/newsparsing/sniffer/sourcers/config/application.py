'''
Created on 4 janv. 2018

@author: tuco
'''
from pyhocon.config_parser import ConfigFactory

# Configuration
configuration = None


def load(configuration_path):
    global configuration
    configuration = ConfigFactory.parse_file(configuration_path)

    
def get_configuration():
    global configuration
    return configuration
