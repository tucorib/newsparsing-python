'''
Created on 5 janv. 2018

@author: tuco
'''
from newsparsing.articles.dao.articles import get_article, store_article, \
    delete_article
from flask_jsonpify import jsonify
from flask.blueprints import Blueprint
from flask.globals import request
article_blueprint = Blueprint('articles', __name__)


def __get_json_data(request):
    if request.headers['Content-Type'] == 'application/json':
        if request.get_json() is None:
            return 'No request JSON data', 400
        return request.get_json()
    else:
        return 'Content-Type must be application/json', 400
    
    
@article_blueprint.route('/article', methods=['POST'])
def article():
    data = __get_json_data(request)
    
    if not 'id' in data:
        return 'No id specified', 403
    if not 'content' in data:
        return 'No content specified', 403
    
    store_article(data['id'], data['content'])
    
    return jsonify({'id': data['id']}), 201

    
@article_blueprint.route('/article/<article_id>', methods=['GET', 'PUT', 'DELETE'])
def article_id(article_id):
    if request.method == 'GET':
        article = get_article(article_id)
        if article is None:
            return 'No article', 404
        else:
            return jsonify(article), 200
    
    elif request.method == 'PUT':
        data = __get_json_data(request)
        
        if not 'content' in data:
            return 'No content specified', 403
        
        store_article(article_id, data['content'])
        
        return jsonify({'id': article_id}), 200

    elif request.method == 'DELETE':
        delete_article(article_id)
        return jsonify({'id': article_id}), 204

        
@article_blueprint.route('/article/<article_id>/<int:version>', methods=['GET'])
def article_id_version(article_id, version):
    article = get_article(article_id, version)
    if article is None:
        return 'No article', 404
    else:
        return jsonify(article), 200
    
