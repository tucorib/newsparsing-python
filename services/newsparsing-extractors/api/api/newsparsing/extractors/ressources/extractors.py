'''
Created on 6 janv. 2018

@author: tuco
'''
from flask.blueprints import Blueprint
from flask.globals import request
from flask.json import jsonify

from core.newsparsing.extractors.constants.extractors import NEWSPAPER3K
from core.newsparsing.extractors.newspaper3k import extract_fields

extractor_blueprint = Blueprint('extractor', __name__)


def __get_json_data(request):
    if request.headers['Content-Type'] == 'application/json':
        if request.get_json() is None:
            return 'No request JSON data', 400
        return request.get_json()
    else:
        return 'Content-Type must be application/json', 400


@extractor_blueprint.route('/<extractor>/extract', methods=['POST'])
def extract(extractor):
    data = __get_json_data(request)

    if not 'fields' in data:
        return 'No field specified', 403

    fields = data['fields']

    if extractor == NEWSPAPER3K:
        return extract_newspaper3k(fields, data)

    return 'Unknwown extractor', 403


def extract_newspaper3k(fields, data):
    if not 'url' in data:
        return 'No url specified', 403
    url = data['url']
    extracts = extract_fields(url, fields)
    return jsonify(extracts), 200
