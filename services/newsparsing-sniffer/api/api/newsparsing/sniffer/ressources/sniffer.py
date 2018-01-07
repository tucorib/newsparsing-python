'''
Created on 6 janv. 2018

@author: tuco
'''
from flask.blueprints import Blueprint
from newsparsing.sniffer.sniffer import sniff as sniff_src
from flask import Response, stream_with_context, json

sniffer_blueprint = Blueprint('sniffer', __name__)


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

    
@sniffer_blueprint.route('/sniff/<source_type>/<source_name>', methods=['GET'])
def sniff(source_type, source_name):
    return Response(stream_json_array(sniff_src(source_type, source_name)), mimetype="application/json")
