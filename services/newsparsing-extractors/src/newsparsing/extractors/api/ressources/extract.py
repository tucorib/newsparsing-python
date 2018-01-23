'''
Created on 6 janv. 2018

@author: tuco
'''
from flask.blueprints import Blueprint
from flask.globals import request
from flask.json import jsonify
from newsparsing.extractors.core.extracts import ExtracterActor

extractor_blueprint = Blueprint('extractor', __name__)


@extractor_blueprint.errorhandler(Exception)
def handle_invalid_usage(error):
    response = jsonify({'error': str(error)})
    response.status_code = 500
    return response


def __get_json_data(request):
    if request.headers['Content-Type'] == 'application/json':
        if request.get_json() is None:
            return 'No request JSON data', 400
        return request.get_json()
    else:
        return 'Content-Type must be application/json', 400


@extractor_blueprint.route('/<extractor>/extract', methods=['POST'])
def extract(extractor):
    # Start actor
    extracter_actor = ExtracterActor.start()

    # Get response
    response = None
    # and exception eventually raised
    exception = None
    try:
        response = jsonify(extracter_actor.ask({**{'extractor': extractor},
                                                **__get_json_data(request)}))
    except Exception as e:
        exception = e
    finally:
        # Stop actor
        extracter_actor.stop()

    # If exception, raise it
    if exception:
        raise exception
    # Return response
    if response:
        return response
