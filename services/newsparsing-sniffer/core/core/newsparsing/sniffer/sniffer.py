'''
Created on 9 janv. 2018

@author: nribeiro
'''
from _io import BytesIO
from queue import Queue
import logging

from flask import json
import ijson
import pykka
import requests

from core.newsparsing.sniffer.config.application import get_service_sourcers, \
    get_source_field_extractors, get_service_extractors, get_source_fields
from core.newsparsing.sniffer.constants.extractors import NEWSPAPER3K
from core.newsparsing.sniffer.errors import MissingMessageKeyException

logger = logging.getLogger('newsparsing.sniffer')


class ArticlesSnifferActor(pykka.ThreadingActor):
    
    def on_start(self):
        pykka.ThreadingActor.on_start(self)
        
        # Create sourcer actor
        self.actor_sourcer = ArticlesSourcerActor.start()
    
    def on_stop(self):
        pykka.ThreadingActor.on_stop(self)
        # Stop sourcer
        self.actor_sourcer.stop()
        
    def on_receive(self, message):
        # Article queue
        queue = Queue()
        # Extractor actors
        self.actors_extractors = {}
        # Launch extractors
        extractors = {}
        for article in self.actor_sourcer.ask(message):
            # Start actor
            extracter_actor = ArticleExtracterActor.start(queue)
            # Register actorRef
            extractors[article['id']] = extracter_actor
            # Ask extraction
            extracter_actor.ask({'article': article},
                                block=False)
        
        # Consume iterator
        try:
            while len(extractors) > 0:
                article = queue.get()
                # Stop extractor actor
                extractors[article['id']].stop()
                # Delete actor
                del extractors[article['id']] 
                # Yield article
                yield article
        finally:
            # Stop extractors
            for actor_extractor in extractors.values():
                actor_extractor.stop()
        
        
class ArticlesSourcerActor(pykka.ThreadingActor):

    def on_receive(self, message):
        if not message.get('source', None):
            raise MissingMessageKeyException('source')

        # Get params
        source = message['source']

        # Get articles from source
        logger.debug('Source articles from %s' % source)
        source_request = requests.get('%s/source/%s/articles' % (get_service_sourcers(),
                                                                 source))

        # Handle error
        if source_request.status_code == 404:
            raise Exception('Service sourcers unavailable')
        if not source_request.status_code == 200:
            raise Exception(json.loads(source_request.content)['error'])

        # Extract articles
        for article in ijson.items(BytesIO(source_request.content), 'item'):
            yield article


class ArticleExtracterActor(pykka.ThreadingActor):

    def __init__(self, queue, *args, **kwargs):
        pykka.ThreadingActor.__init__(self, *args, **kwargs)
        self.queue = queue

    def on_receive(self, message):
        if not message.get('article', None):
            raise MissingMessageKeyException('article')

        article = message['article']
        source = article['source']

        # Get fields to extract
        fields = get_source_fields(source)
        # Get extractors for source
        extractors = set()
        for field in fields:
            extractors = extractors.union(get_source_field_extractors(source,
                                                                      field))
        # Get extracts
        extracts = {}
        for extractor in extractors:
            # Request data
            params = {
                'fields': fields
            }

            self.__build_params(article, extractor, params)

            # Request
            logger.debug('Extract article %s' % article['id'])
            extract_request = requests.post('%s/extractor/%s/extract' % (get_service_extractors(),
                                                                         extractor),
                                            data=json.dumps(params),
                                            headers={'Content-Type': 'application/json'})

            # Handle error
            if extract_request.status_code == 404:
                raise Exception('Service extractors unavailable')
            if not extract_request.status_code == 200:
                raise Exception(extract_request.content)

            # Store extracts
            extracts[extractor] = extract_request.json()

        # Build content
        content = {}
        for field in fields:
            for extractor in get_source_field_extractors(source, field):
                content[field] = extracts[extractor][field]

        # Return extracts
        self.queue.put({'id': article['id'], 'content': content})

    def __build_params(self, article, extractor, params):
        if extractor == NEWSPAPER3K:
            params['url'] = article['url']
