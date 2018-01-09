'''
Created on 6 janv. 2018

@author: tuco
'''
from flask import Response, stream_with_context, json
from flask.blueprints import Blueprint

from core.newsparsing.sourcers.config.rss import get_rss_sources, \
    get_rss_source_sourcer
from core.newsparsing.sourcers.constants.source_type import RSS
from core.newsparsing.sourcers.constants.sourcers import FEEDPARSER
from core.newsparsing.sourcers.rss.feedparser import get_feedparser_articles

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


@source_blueprint.route('/articles/<source_type>/<source_name>',
                        methods=['GET'])
def articles(source_type, source_name):
    if source_type == RSS:
        if source_name in get_rss_sources():
            sourcer = get_rss_source_sourcer(source_name)
            if sourcer == FEEDPARSER:
                return Response(
                    stream_json_array(get_feedparser_articles(source_name)),
                    mimetype="application/json")
            else:
                return 'Sourcer unknown', 404
        else:
            return 'Source unknown', 404
    else:
        return 'Source type unknown', 404
