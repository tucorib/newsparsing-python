'''
Created on 7 janv. 2018

@author: tuco
'''
import argparse
import os

from api.newsparsing.articles.flask_app import create_flask_app, \
    load_flask_configuration
from core.newsparsing.articles.config.application import load_configuration

if __name__ == '__main__':
    # Arguments
    parser = argparse.ArgumentParser(
        description='Launch newsparsing-articles flask API.'
    )
    parser.add_argument('-c',
                        '--config',
                        dest='articles_configuration',
                        default=os.path.join(os.path.dirname(__file__),
                                             "../conf/application.conf"),
                        help='newsparsing-articles configuration ')
    parser.add_argument('-f',
                        '--flask',
                        dest='flask_configuration',
                        default=os.path.join(os.path.dirname(__file__),
                                             "../conf/flask.conf"),
                        help='newsparsing-articles flask configuration')
    args = parser.parse_args()

    # Load articles configuration
    load_configuration(args.articles_configuration)
    # Create flask API
    flask_app = create_flask_app()
    # Load configuration
    load_flask_configuration(flask_app,
                             args.flask_configuration)
    # Start API
    flask_app.run()
