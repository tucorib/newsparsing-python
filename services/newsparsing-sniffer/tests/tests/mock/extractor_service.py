'''
Created on 17 janv. 2018

@author: nribeiro
'''

import threading

from flask import jsonify, request
from flask.app import Flask
import requests

from core.newsparsing.sniffer.config.application import get_service_extractors

TEST_UNKNOWN_EXTRACTOR = 'unknown-extractor'
TEST_EXTRACTOR = 'newspaper3k'
TEST_FIELDS = ['title', 'text', 'authors', 'url']

# Flask app
flask_app = Flask(__name__)


@flask_app.route('/extractor/%s/extract' % TEST_UNKNOWN_EXTRACTOR,
                 methods=['POST'])
def unknown_extractor(extractor):
    return jsonify({'error': 'Unknown extractor %s' % extractor}), 500


@flask_app.route('/shutdown', methods=['POST'])
def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

    
def start_extractor_mock():
    # Set configuration
    flask_app.config['SERVER_NAME'] = get_service_extractors()

    # Start API
    thread = threading.Thread(target=flask_app.run, args=())
    thread.daemon = True
    thread.start()


def stop_extractor_mock():
    requests.post('%s/shutdown' % get_service_extractors())
