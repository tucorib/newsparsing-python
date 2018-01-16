'''
Created on 9 janv. 2018

@author: nribeiro
'''
from _io import BytesIO
from queue import Queue
import json
import logging

import ijson
import pykka
import requests

from core.newsparsing.sniffer.config.application import get_service_sourcers
from core.newsparsing.sniffer.errors import MissingMessageKeyException
from core.newsparsing.sniffer.extracter import ArticleExtracterActor

logger = logging.getLogger('newsparsing.sniffer')


class ArticlesIterator:

    actorsRef = {}
    readys = Queue()

    def ask(self, parentActor, article):
        # Start actor
        extracter_actor = ArticleExtracterActor.start(parentActor)
        # Ask extraction
        extracter_actor.ask({'article': article},
                            block=False)
        # Register actorRef
        self.actorsRef[article['id']] = extracter_actor

    def answer(self, _id, content):
        # Get actor ref
        actorRef = self.actorsRef[_id]
        # Stop actor
        actorRef.stop()
        # Remove actor
        del self.actorsRef[_id]
        # Add content
        self.readys.put({'id': _id, 'content': content})

    def __iter__(self):
        return self

    def __next__(self):
        # Raise stop iteration if no article pending
        if len(self.actorsRef) == 0:
            raise StopIteration

        # Pop a ready article
        return self.readys.get()


class ArticlesSnifferActor(pykka.ThreadingActor):

    def on_receive(self, message):
        if not message.get('command', None):
            raise MissingMessageKeyException('command')

        command = message.get('command')

        if command == 'sniff':
            return self.__sniff(message)
        if command == 'extract':
            return self.__extract(message)

    def __sniff(self, message):
        if not message.get('source', None):
            raise MissingMessageKeyException('source')

        # Create async iterator
        self.iterator = ArticlesIterator()

        # Get params
        source = message['source']

        # Get articles from source
        logger.debug('Source articles from %s' % source)
        source_request = requests.get('%s/source/%s/articles' % (get_service_sourcers(),
                                                                 source))

        # Handle error
        if not source_request.status_code == 200:
            raise Exception(json.loads(source_request.content)['error'])

        # Extract articles
        for article in ijson.items(BytesIO(source_request.content), 'item'):
            self.iterator.ask(self, article)

        # Return contents
        for article in self.iterator:
            yield article

    def __extract(self, message):
        if not message.get('id', None):
            raise MissingMessageKeyException('id')
        if not message.get('content', None):
            raise MissingMessageKeyException('content')

        # Add extract to iterator
        self.iterator.answer(message['id'], message['content'])
