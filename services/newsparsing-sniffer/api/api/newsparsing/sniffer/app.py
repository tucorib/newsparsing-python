'''
Created on 5 janv. 2018

@author: tuco
'''
from flask import Flask
from api.newsparsing.sniffer.ressources.sniffer import sniffer_blueprint
import logging.config
from newsparsing.sniffer.config.application import load
import os
import argparse


def create_app(configuration_filename=None):
    flask_app = Flask(__name__)
    
    # Configuration
    if configuration_filename:
        flask_app.config.from_pyfile(configuration_filename)
        
    # Logger
    if flask_app.config.get('LOGGER', None):
        flask_app.logger_name = 'newsparsing.sniffer.api'
        logging.config.fileConfig(flask_app.config['LOGGER'])
        
    # Blueprints
    flask_app.register_blueprint(sniffer_blueprint)
    
    # Log creation
    flask_app.logger.debug('sniffer flask created')
    
    return flask_app


if __name__ == '__main__':
    # Arguments
    parser = argparse.ArgumentParser(description='Launch newsparsing-sniffer flask app.')
    parser.add_argument('-c',
                        '--config',
                        dest='sniffer_configuration',
                        default=os.path.join(os.path.dirname(__file__), "../../../../conf/application.conf"),
                        help='newsparsing-sniffer configuration file path')
    parser.add_argument('-f',
                        '--flask',
                        dest='flask_configuration',
                        default=os.path.join(os.path.dirname(__file__), "../../../../conf/flask.conf"),
                        help='newsparsing-sniffer flask configuration file path')
    args = parser.parse_args()
    
    # Get sniffer configuration path
    sniffer_configuration = args.sniffer_configuration
    # Get flask configuration path
    flask_configuration = args.flask_configuration
    
    load(sniffer_configuration)
    create_app(flask_configuration).run()