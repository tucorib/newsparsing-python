'''
Created on 17 janv. 2018

@author: nribeiro
'''
import threading

from flask import jsonify, request
from flask.app import Flask
import requests

from core.newsparsing.sniffer.config.application import get_service_sourcers

TEST_UNKNOWN_SOURCE = 'unknown-source'
TEST_NO_SOURCER = 'no-sourcer'
TEST_NO_URL = 'no-url'
TEST_UNKNOWN_SOURCER = 'unknown-sourcer'
TEST_SOURCE = 'test'

# Flask app
flask_app = Flask(__name__)


@flask_app.route('/source/%s/articles' % TEST_UNKNOWN_SOURCE,
                 methods=['GET'])
def unknown_source(source):
    return jsonify({'error': 'Unknown source %s' % source}), 500


@flask_app.route('/source/%s/articles' % TEST_NO_SOURCER,
                 methods=['GET'])
def no_sourcer(source):
    return jsonify({'error': 'Source %s has no sourcer' % source}), 500


@flask_app.route('/source/%s/articles' % TEST_NO_URL,
                 methods=['GET'])
def no_url(source):
    return jsonify({'error': 'Source %s has no url' % source}), 500


@flask_app.route('/source/%s/articles' % TEST_UNKNOWN_SOURCER,
                 methods=['GET'])
def unknown_sourcer(source):
    return jsonify({'error': 'Source %s has an unknown sourcer' % source}), 500


@flask_app.route('/source/%s/articles' % TEST_SOURCE,
                 methods=['GET'])
def test_source(source):
    return jsonify({'error': 'Source %s has an unknown sourcer' % source}), 200


@flask_app.route('/shutdown', methods=['POST'])
def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


def start_sourcer_mock():
    # Set configuration
    flask_app.config['SERVER_NAME'] = get_service_sourcers()
    # Start API
    thread = threading.Thread(target=flask_app.run, args=())
    thread.daemon = True
    thread.start()


def stop_sourcer_mock():
    requests.post('%s/shutdown' % get_service_sourcers())
