'''
Created on 6 janv. 2018

@author: tuco
'''
from flask.blueprints import Blueprint
from newsparsing.sniffer.sniffer import sniff as sniff_src
from flask import Response
from flask.json import jsonify

sniffer_blueprint = Blueprint('sniffer', __name__)


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

    
@sniffer_blueprint.route('/sniff/<source_type>/<source_name>', methods=['GET'])
def sniff(source_type, source_name):
    return Response(stream_json_array(sniff_src(source_type, source_name), 'articles'), mimetype="application/json")
