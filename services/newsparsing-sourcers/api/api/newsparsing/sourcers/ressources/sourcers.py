'''
Created on 6 janv. 2018

@author: tuco
'''
from flask import Response, stream_with_context, json, jsonify
from flask.blueprints import Blueprint
from core.newsparsing.sourcers.articles import ArticlesActor

source_blueprint = Blueprint('source', __name__)


@source_blueprint.errorhandler(Exception)
def handle_invalid_usage(error):
    response = jsonify({'error': str(error)})
    response.status_code = 500
    return response


def stream_iterator(iterator):
    # Get first element
    first = next(iterator)
    if first is None:
        # Empty queue, return empty JSON
        return Response(json.dumps({}),
                        mimetype="application/json")

    def stream(iterator):
        yield '[%s' % json.dumps(first)
        for item in iterator:
            yield ', %s' % json.dumps(item)
        yield ']'

    return Response(stream_with_context(stream(iterator)),
                    mimetype="application/json")


@source_blueprint.route('/<source>/articles',
                        methods=['GET'])
def articles(source):
    # Start actor
    articles_actor = ArticlesActor.start()

    # Get response for streaming
    response = None
    # and exception eventually raised
    exception = None
    try:
        response = stream_iterator(articles_actor.ask({'source': source}))
    except Exception as e:
        exception = e
    finally:
        # Stop actor
        articles_actor.stop()

    # If exception, raise it
    if exception:
        raise exception
    # Return response
    if response:
        return response
