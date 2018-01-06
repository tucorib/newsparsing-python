'''
Created on 5 janv. 2018

@author: tuco
'''
from flask import Flask
from api.newsparsing.extractors.ressources.extractors import extractor_blueprint
import logging.config
from newsparsing.extractors.config.application import load
import os
import argparse


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


if __name__ == '__main__':
    # Arguments
    parser = argparse.ArgumentParser(description='Launch newsparsing-extractors flask app.')
    parser.add_argument('-c',
                        '--config',
                        dest='extractors_configuration',
                        default=os.path.join(os.path.dirname(__file__), "../../../../conf/application.conf"),
                        help='newsparsing-extractors configuration file path')
    parser.add_argument('-f',
                        '--flask',
                        dest='flask_configuration',
                        default=os.path.join(os.path.dirname(__file__), "../../../../conf/flask.conf"),
                        help='newsparsing-extractors flask configuration file path')
    args = parser.parse_args()
    
    # Get extractors configuration path
    extractors_configuration = args.extractors_configuration
    # Get flask configuration path
    flask_configuration = args.flask_configuration
    
    load(extractors_configuration)
    create_app(flask_configuration).run()