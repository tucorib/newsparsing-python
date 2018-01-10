'''
Created on 6 janv. 2018

@author: tuco
'''
from flask import Response, stream_with_context, json
from flask.blueprints import Blueprint

from core.newsparsing.sourcers.config.application import get_sources
from core.newsparsing.sourcers.sourcer import get_articles

source_blueprint = Blueprint('source', __name__)


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


@source_blueprint.route('/<source>/articles',
                        methods=['GET'])
def articles(source):
    if source in get_sources():
        return Response(
                    stream_json_array(get_articles(source)),
                    mimetype="application/json")
    else:
        return 'Source unknown', 404
