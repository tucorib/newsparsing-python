'''
Created on 5 janv. 2018

@author: tuco
'''
from flask import Flask
from api.newsparsing.extractors.ressources.extractors import extractor_blueprint
import logging.config


def create_app(configuration_filename=None):
    flask_app = Flask(__name__)
    
    # Configuration
    if configuration_filename:
        flask_app.config.from_pyfile(configuration_filename)
        
    # Logger
    if flask_app.config.get('LOGGER', None):
        flask_app.logger_name = 'newsparsing.extractors.api'
        logging.config.fileConfig(flask_app.config['LOGGER'])
        
    # Blueprints
    flask_app.register_blueprint(extractor_blueprint)
    
    # Log creation
    flask_app.logger.debug('extractors flask created')
    
    return flask_app

