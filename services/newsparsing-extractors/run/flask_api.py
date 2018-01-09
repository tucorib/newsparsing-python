'''
Created on 7 janv. 2018

@author: tuco
'''
import argparse
import os

from api.newsparsing.extractors.flask_app import create_flask_app, \
    load_flask_configuration
from core.newsparsing.extractors.config.application import load_configuration

if __name__ == '__main__':
    # Arguments
    parser = argparse.ArgumentParser(
        description='Launch newsparsing-extractors flask API.'
    )
    parser.add_argument('-c',
                        '--config',
                        dest='extractors_configuration',
                        default=os.path.join(os.path.dirname(__file__),
                                             "../conf/application.conf"),
                        help='newsparsing-extractors configuration ')
    parser.add_argument('-f',
                        '--flask',
                        dest='flask_configuration',
                        default=os.path.join(os.path.dirname(__file__),
                                             "../conf/flask.conf"),
                        help='newsparsing-extractors flask configuration')
    args = parser.parse_args()

    # Load sourcers configuration
    load_configuration(args.sourcers_configuration)
    # Create flask API
    flask_app = create_flask_app()
    # Load configuration
    load_flask_configuration(flask_app,
                             args.flask_configuration)
    # Start API
    flask_app.run()
