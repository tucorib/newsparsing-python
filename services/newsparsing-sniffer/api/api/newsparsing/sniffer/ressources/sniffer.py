'''
Created on 6 janv. 2018

@author: tuco
'''
from flask.blueprints import Blueprint
from flask.json import jsonify
from newsparsing.sniffer.sniffer import sniff as sniff_src

sniffer_blueprint = Blueprint('sniffer', __name__)

    
@sniffer_blueprint.route('/sniff/<source_type>/<source_name>', methods=['GET'])
def sniff(source_type, source_name):
    articles = [_ for _ in sniff_src(source_type, source_name)]
    return jsonify(articles), 200
