'''
Created on 6 janv. 2018

@author: tuco
'''
from flask import json
from flask.blueprints import Blueprint
from flask.helpers import stream_with_context
from flask.wrappers import Response
from core.newsparsing.sniffer.articles_sniffer import ArticlesSnifferActor

sniffer_blueprint = Blueprint('sniffer', __name__)


@stream_with_context
def stream_json_array(iterator):
    try:
        prev = next(iterator)  # Get first result
    except StopIteration:
        # Empty iterator, return now
        yield '[]'
        raise StopIteration

    yield '['
    # Iterate
    for _ in iterator:
        yield '%s, ' % json.dumps(_)
        prev = _
    # Now yield the last iteration without comma but with the closing brackets
    yield '%s]' % json.dumps(prev)


@sniffer_blueprint.route('/<source>',
                         methods=['GET'])
def sniff(source):
    # Create iterator
    articles_sniffer = ArticlesSnifferActor.start()
    articles_iterator = articles_sniffer.ask({'source': source})
    # Stop actor
    articles_sniffer.stop()

    return Response(stream_json_array(articles_iterator),
                    mimetype="application/json")
