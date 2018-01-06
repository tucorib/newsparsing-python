'''
Created on 6 janv. 2018

@author: tuco
'''
from flask.blueprints import Blueprint
from newsparsing.sourcers import SourceType
from newsparsing.sourcers.source import get_articles
from newsparsing.sourcers.config.rss import get_rss_sources
from flask import Response
from flask.json import jsonify

source_blueprint = Blueprint('sources', __name__)


def stream_json_array(iterator, field_name):
    try:
        prev = next(iterator)  # Get first result
    except StopIteration:
        # Empty iterator, return now
        yield '{"%s": []}' % field_name
        raise StopIteration
    
    yield '{"%s": [' % field_name
    # Iterate
    for _ in iterator:
        yield jsonify(_) + ', '
        prev = _
    # Now yield the last iteration without comma but with the closing brackets
    yield jsonify(prev) + ']}'

        
@source_blueprint.route('/articles/<source_type>/<source_name>', methods=['GET'])
def articles(source_type, source_name):
    if source_type == SourceType.RSS:
        if source_name in get_rss_sources():
            return Response(stream_json_array(get_articles(source_type, source_name), 'articles'), mimetype="application/json")
        else:
            return 'Source unknown', 404
    else:
        return 'Source type unknown', 404
