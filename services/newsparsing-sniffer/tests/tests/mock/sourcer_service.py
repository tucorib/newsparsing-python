'''
Created on 17 janv. 2018

@author: nribeiro
'''
import threading

from flask import Response, stream_with_context, json, jsonify, request
from flask.app import Flask
import requests

TEST_UNKNOWN_SOURCE = 'unknown-source'
TEST_NO_SOURCER = 'no-sourcer'
TEST_NO_URL = 'no-url'
TEST_UNKNOWN_SOURCER = 'unknown-sourcer'
TEST_SOURCE = 'test'

# Flask app
flask_app = Flask(__name__)


def stream_iterator(iterator):
    try:
        # Get first element
        first = next(iterator)
    except StopIteration:
        # Empty queue, return empty JSON
        return Response(json.dumps([]),
                        mimetype="application/json")

    def stream(iterator):
        yield '[%s' % json.dumps(first)
        for item in iterator:
            yield ', %s' % json.dumps(item)
        yield ']'

    return Response(stream_with_context(stream(iterator)),
                    mimetype="application/json")


@flask_app.route('/source/<source>/articles',
                 methods=['GET'])
def articles(source):
    if source == TEST_UNKNOWN_SOURCE:
        return jsonify({'error': 'Unknown source %s' % source}), 500
    if source == TEST_NO_SOURCER:
        return jsonify({'error': 'Source %s has no sourcer' % source}), 500
    if source == TEST_NO_URL:
        return jsonify({'error': 'Source %s has no url' % source}), 500
    if source == TEST_UNKNOWN_SOURCER:
        return jsonify({'error': 'Source %s has an unknown sourcer' % source}), 500
    if source == TEST_SOURCE:
        return stream_iterator(iter([
            {'source': TEST_SOURCE,
             'id': 'article id',
             'url': 'article url'
             }
        ]))


@flask_app.route('/source/<source>/articles/<int:limit>',
                 methods=['GET'])
def articles_limit(source, limit):
    if source == TEST_UNKNOWN_SOURCE:
        return jsonify({'error': 'Unknown source %s' % source}), 500
    if source == TEST_NO_SOURCER:
        return jsonify({'error': 'Source %s has no sourcer' % source}), 500
    if source == TEST_NO_URL:
        return jsonify({'error': 'Source %s has no url' % source}), 500
    if source == TEST_UNKNOWN_SOURCER:
        return jsonify({'error': 'Source %s has an unknown sourcer' % source}), 500
    if source == TEST_SOURCE:
        return stream_iterator(iter([
            {'source': TEST_SOURCE,
             'id': 'article id %d' % _,
             'url': 'article url'
             } for _ in range(0, limit)
        ]))


@flask_app.route('/shutdown', methods=['POST'])
def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return jsonify({})


def start_sourcer_mock():
    # Set configuration
    flask_app.config['SERVER_NAME'] = 'localhost:5000'
    # Start API
    thread = threading.Thread(target=flask_app.run, args=())
    thread.daemon = True
    thread.start()


def stop_sourcer_mock():
    requests.post('http://localhost:5000/shutdown')
