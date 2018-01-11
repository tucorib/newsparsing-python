'''
Created on 6 janv. 2018

@author: tuco
'''
from flask.blueprints import Blueprint
from flask.globals import request
from flask.json import jsonify

from core.newsparsing.extractors.extracts import ExtracterActor

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
    del data['fields']
    params = data

    # Start actor
    extracter_actor = ExtracterActor.start()
    extracter_result = extracter_actor.ask({**{'extractor': extractor,
                                               'fields': fields},
                                            **params})

    # Stop actor
    extracter_actor.stop()

    # Parse result
    if not extracter_result.get('error', None) is None:
        return extracter_result['error'], 403

    return jsonify(extracter_result)
