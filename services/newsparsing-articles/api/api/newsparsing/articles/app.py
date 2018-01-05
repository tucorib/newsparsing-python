'''
Created on 5 janv. 2018

@author: tuco
'''
from flask import Flask
from api.newsparsing.articles.ressources.articles import article_blueprint
from newsparsing.articles.config.application import load
import sys
import logging.config


def create_app(configuration_filename=None):
    flask_app = Flask(__name__)
    
    # Configuration
    if configuration_filename:
        flask_app.config.from_pyfile(configuration_filename)
        
    # Logger
    if flask_app.config.get('LOGGER', None):
        flask_app.logger_name = 'newsparsing.articles.api'
        logging.config.fileConfig(flask_app.config['LOGGER'])
        
    # Blueprints
    flask_app.register_blueprint(article_blueprint)
    
    # Log creation
    flask_app.logger.debug('articles flask created')
    
    return flask_app


if __name__ == '__main__':
    # Check configuration argument
    if len(sys.argv) < 3:
        sys.stderr.write('Configuration argument is not passed')
        exit(-1)
    
    # Get articles configuration path
    articles_configuration = sys.argv[1]
    # Get flask configuration path
    flask_configuration = sys.argv[2]
    
    load(articles_configuration)
    create_app(flask_configuration).run()
