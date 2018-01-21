'''
Created on 6 janv. 2018

@author: tuco
'''
from flask import json, jsonify
from flask.blueprints import Blueprint
from flask.helpers import stream_with_context
from flask.wrappers import Response
from core.newsparsing.sniffer.sniffer import ArticlesSnifferActor

sniffer_blueprint = Blueprint('sniffer', __name__)


@sniffer_blueprint.errorhandler(Exception)
def handle_invalid_usage(error):
    response = jsonify({'error': str(error)})
    response.status_code = 500
    return response


def stream_iterator(iterator):
    # Get first element
    first = next(iterator)
    if first is None:
        # Empty queue, return empty JSON
        return Response(json.dumps({}),
                        mimetype="application/json")

    def stream(iterator):
        yield '[%s' % json.dumps(first)
        for item in iterator:
            yield ', %s' % json.dumps(item)
        yield ']'

    return Response(stream_with_context(stream(iterator)),
                    mimetype="application/json")


@sniffer_blueprint.route('/<source>',
                         methods=['GET'])
def sniff(source):
    # Start actor
    sniffer_actor = ArticlesSnifferActor.start()

    # Get response for streaming
    response = None
    # and exception eventually raised
    exception = None

    try:
        response = stream_iterator(sniffer_actor.ask({'source': source}))
    except Exception as e:
        exception = e
    finally:
        # Stop actor
        sniffer_actor.stop()

    # If exception, raise it
    if exception:
        raise exception
    # Return response
    if response:
        return response
