'''
Created on 11 janv. 2018

@author: nribeiro
'''
import pykka

from newsparsing.sourcers.core.config.application import get_sources, \
    get_source_sourcer
from newsparsing.sourcers.core.constants.sourcers import FEEDPARSER
from newsparsing.sourcers.core.errors import MissingMessageKeyException, \
    UnknownSourceException, NoSourcerException, UnknownSourcerException
from newsparsing.sourcers.core.sourcers.feedparser import FeedparserActor


class ArticlesActor(pykka.ThreadingActor):

    def on_receive(self, message):
        # Check source argument
        if not message.get('source', None):
            raise MissingMessageKeyException('source')

        source = message['source']
        limit = message.get('limit', None)

        # Check source
        if source not in get_sources():
            raise UnknownSourceException(source)

        # Get sourcer
        sourcer = get_source_sourcer(source)

        # Check sourcer
        if not sourcer:
            raise NoSourcerException(source)

        # Start actor according to sourcer
        if sourcer == FEEDPARSER:
            # Start actor
            parser_actor = FeedparserActor.start(self)
            try:
                for article in parser_actor.ask({'source': source,
                                                 'limit': limit}):
                    yield article
            finally:
                # Stop actor
                parser_actor.stop()
        else:
            # If here, it means that sourcer is unknown
            raise UnknownSourcerException(sourcer)
