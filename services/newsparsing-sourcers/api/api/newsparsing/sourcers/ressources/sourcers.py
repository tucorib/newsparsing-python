'''
Created on 6 janv. 2018

@author: tuco
'''
from flask import Response, stream_with_context, json
from flask.blueprints import Blueprint

from core.newsparsing.sourcers.core import SourceType
from core.newsparsing.sourcers.core.config.rss import get_rss_sources
from core.newsparsing.sourcers.core.source import get_articles

source_blueprint = Blueprint('sources', __name__)


@stream_with_context
def stream_json_array(iterator):
    try:
        prev = next(iterator)  # Get first result
    except StopIteration:
        # Empty iterator, return now
        yield '[]}'
        raise StopIteration
    
    yield '['
    # Iterate
    for _ in iterator:
        yield '%s, ' % json.dumps(_)
        prev = _
    # Now yield the last iteration without comma but with the closing brackets
    yield '%s]' % json.dumps(prev)

        
@source_blueprint.route('/articles/<source_type>/<source_name>', methods=['GET'])
def articles(source_type, source_name):
    if source_type == SourceType.RSS:
        if source_name in get_rss_sources():
            return Response(stream_json_array(get_articles(source_type, source_name)), mimetype="application/json")
        else:
            return 'Source unknown', 404
    else:
        return 'Source type unknown', 404
