'''
Created on 5 janv. 2018

@author: tuco
'''
from flask import Flask
from newsparsing.sourcers.api.ressources.sourcers import source_blueprint


def create_flask_app():
    # Flask app
    flask_app = Flask(__name__)
    # Flask app blueprints
    flask_app.register_blueprint(source_blueprint, url_prefix='/source')

    return flask_app


def load_flask_configuration(flask_app, flask_configuration_file=None):
    if flask_configuration_file is not None:
        # Configuration
        flask_app.config.from_pyfile(flask_configuration_file)
