'''
Created on 5 janv. 2018

@author: tuco
'''
import logging.config

from flask import Flask
from newsparsing.sniffer.api.ressources.sniffer import sniffer_blueprint


def create_flask_app():
    # Flask app
    flask_app = Flask(__name__)
    # Flask app blueprints
    flask_app.register_blueprint(sniffer_blueprint, url_prefix='/sniff')

    return flask_app


def load_flask_configuration(flask_app, flask_configuration_file=None):
    if flask_configuration_file is not None:
        # Configuration
        flask_app.config.from_pyfile(flask_configuration_file)

        # Logger
        if flask_app.config.get('LOGGER', None):
            flask_app.logger_name = 'newsparsing.sniffer.api'
            logging.config.fileConfig(flask_app.config['LOGGER'])
