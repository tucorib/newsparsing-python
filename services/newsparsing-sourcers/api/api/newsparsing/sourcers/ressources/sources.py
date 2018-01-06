'''
Created on 6 janv. 2018

@author: tuco
'''
from flask.blueprints import Blueprint
from newsparsing.sourcers import SourceType
from newsparsing.sourcers.source import get_articles
from flask.json import jsonify
from newsparsing.sourcers.config.rss import get_rss_sources

source_blueprint = Blueprint('sources', __name__)


@source_blueprint.route('/articles/<source_type>/<source_name>', methods=['GET'])
def articles(source_type, source_name):
    if source_type == SourceType.RSS:
        if source_name in get_rss_sources():
            articles = [_ for _ in get_articles(source_type, source_name)]
            return jsonify(articles), 200
        else:
            return 'Source unknown', 404
    else:
        return 'Source type unknown', 404
