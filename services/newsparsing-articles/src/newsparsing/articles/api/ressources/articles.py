'''
Created on 5 janv. 2018

@author: tuco
'''
from flask.blueprints import Blueprint
from flask.globals import request
from flask_jsonpify import jsonify

from newsparsing.articles.core.dao.article_deleter import ArticleDeleterActor
from newsparsing.articles.core.dao.article_getter import ArticleGetterActor
from newsparsing.articles.core.dao.article_storer import ArticleStorerActor

article_blueprint = Blueprint('article', __name__)


def __get_json_data(request):
    if request.headers['Content-Type'] == 'application/json':
        if request.get_json() is None:
            return 'No request JSON data', 400
        return request.get_json()
    else:
        return 'Content-Type must be application/json', 400


@article_blueprint.route('',
                         methods=['POST'])
def article():
    data = __get_json_data(request)

    if not 'id' in data:
        return 'No id specified', 403
    if not 'content' in data:
        return 'No content specified', 403

    # Start actor
    article_storer_actor = ArticleStorerActor.start()
    version = article_storer_actor.ask({'id': data['id'],
                                        'content': data['content']
                                        })
    # Stop actor
    article_storer_actor.stop()

    if version == 0:
        return jsonify({'id': data['id'], 'version': version}), 201
    else:
        return jsonify({'id': data['id'], 'version': version}), 200


@article_blueprint.route('/<article_id>',
                         methods=['GET', 'DELETE'])
def article_id(article_id):
    if request.method == 'GET':
        # Start actor
        article_getter_actor = ArticleGetterActor.start()
        article = article_getter_actor.ask({'id': article_id})
        # Stop actor
        article_getter_actor.stop()

        if article is None:
            return 'No article', 404
        else:
            return jsonify(article), 200

    elif request.method == 'DELETE':
        # Start actor
        article_deleter_actor = ArticleDeleterActor.start()
        article_deleter_actor.ask({'id': article_id},
                                  block=False)
        # Stop actor
        article_deleter_actor.stop()

        return jsonify({'id': article_id}), 204


@article_blueprint.route('/<article_id>/<int:version>',
                         methods=['GET'])
def article_id_version(article_id, version):
    # Start actor
    article_getter_actor = ArticleGetterActor().start()
    article = article_getter_actor.ask({'id': article_id,
                                        'version': version})
    # Stop actor
    article_getter_actor.stop()

    if article is None:
        return 'No article', 404
    else:
        return jsonify(article), 200

