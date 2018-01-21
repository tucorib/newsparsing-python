'''
Created on 17 janv. 2018

@author: nribeiro
'''

import threading

from flask import jsonify, request
from flask.app import Flask
import requests

TEST_UNKNOWN_EXTRACTOR = 'unknown-extractor'
TEST_EXTRACTOR = 'newspaper3k'
TEST_FIELDS = ['title', 'text', 'authors', 'url']

# Flask app
flask_app = Flask(__name__)


def __get_json_data(request):
    if request.headers['Content-Type'] == 'application/json':
        if request.get_json() is None:
            return 'No request JSON data', 400
        return request.get_json()
    else:
        return 'Content-Type must be application/json', 400

    
@flask_app.route('/extractor/<extractor>/extract',
                 methods=['POST'])
def extract(extractor):
    if extractor == TEST_UNKNOWN_EXTRACTOR:
        return jsonify({'error': 'Unknown extractor %s' % extractor}), 500
    if extractor == TEST_EXTRACTOR:
        params = __get_json_data(request)
        
        if set(params['fields']) == set(TEST_FIELDS) and params['url'] == 'article url':
            return jsonify(
                {'title': 'article title',
                 'text': 'article text',
                 'authors': ['article authors'],
                 'url': params['url']
                 }
            )
        else:
            return jsonify({'error': 'Wrong parameters: %s' % str(params)}), 500


@flask_app.route('/shutdown', methods=['POST'])
def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return jsonify({})

    
def start_extractor_mock():
    # Set configuration
    flask_app.config['SERVER_NAME'] = 'localhost:5001'

    # Start API
    thread = threading.Thread(target=flask_app.run, args=())
    thread.daemon = True
    thread.start()


def stop_extractor_mock():
    requests.post('http://localhost:5001/shutdown')
