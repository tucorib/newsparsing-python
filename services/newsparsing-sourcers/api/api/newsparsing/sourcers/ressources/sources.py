'''
Created on 6 janv. 2018

@author: tuco
'''
from flask.blueprints import Blueprint
from flask.globals import request
from newsparsing.sourcers import SourceType
from newsparsing.sourcers.source import get_articles
from flask.json import jsonify

source_blueprint = Blueprint('sources', __name__)


@source_blueprint.route('/articles/<source_type>/<source_name>', methods=['GET'])
def articles(source_type, source_name):
    if request.method == 'GET':
        if source_type == SourceType.RSS:
            articles = get_articles(source_type, source_name)
            return jsonify(articles), 200
    else:
        return 'Source type unknown', 404
