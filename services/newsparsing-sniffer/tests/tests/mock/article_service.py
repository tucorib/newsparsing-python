'''
Created on 17 janv. 2018

@author: nribeiro
'''
import threading

from flask import jsonify
from flask.app import Flask
from flask.globals import request
import requests

# Flask app
flask_app = Flask(__name__)


def __get_json_data(request):
    if request.headers['Content-Type'] == 'application/json':
        if request.get_json() is None:
            return 'No request JSON data', 400
        return request.get_json()
    else:
        return 'Content-Type must be application/json', 400


@flask_app.route('/article',
                 methods=['POST'])
def article():
    data = __get_json_data(request)

    if 'id' not in data:
        return 'No id specified', 403
    if 'content' not in data:
        return 'No content specified', 403

    return jsonify({'id': data['id'], 'version': 0}), 200


@flask_app.route('/shutdown', methods=['POST'])
def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return jsonify({})


def start_articles_mock():
    # Set configuration
    flask_app.config['SERVER_NAME'] = 'localhost:5002'
    # Start API
    thread = threading.Thread(target=flask_app.run, args=())
    thread.daemon = True
    thread.start()


def stop_articles_mock():
    requests.post('http://localhost:5002/shutdown')
