'''
Created on 5 janv. 2018

@author: tuco
'''
from flask import Flask
from api.newsparsing.sourcers.ressources.sources import source_blueprint
import logging.config
from newsparsing.sourcers.config.application import load
import os


def create_app(configuration_filename=None):
    flask_app = Flask(__name__)
    
    # Configuration
    if configuration_filename:
        flask_app.config.from_pyfile(configuration_filename)
        
    # Logger
    if flask_app.config.get('LOGGER', None):
        flask_app.logger_name = 'newsparsing.sourcers.api'
        logging.config.fileConfig(flask_app.config['LOGGER'])
        
    # Blueprints
    flask_app.register_blueprint(source_blueprint)
    
    # Log creation
    flask_app.logger.debug('sourcers flask created')
    
    return flask_app


if __name__ == '__main__':
    # Get sourcers configuration path
    sourcers_configuration = os.path.join(os.path.dirname(__file__), "../../../../conf/test.application.conf")
    # Get flask configuration path
    flask_configuration = os.path.join(os.path.dirname(__file__), "../../../../conf/test.flask.conf")
    
    load(sourcers_configuration)
    create_app(flask_configuration).run()