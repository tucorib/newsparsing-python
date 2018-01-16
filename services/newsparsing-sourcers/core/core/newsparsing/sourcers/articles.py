'''
Created on 11 janv. 2018

@author: nribeiro
'''
import pykka

from core.newsparsing.sourcers.config.application import get_source_sourcer, \
    get_sources
from core.newsparsing.sourcers.constants.sourcers import FEEDPARSER
from core.newsparsing.sourcers.errors import MissingMessageKeyException, \
    UnknownSourceException, NoSourcerException, UnknownSourcerException
from core.newsparsing.sourcers.sourcers.feedparser import FeedparserActor


class ArticlesActor(pykka.ThreadingActor):

    def on_receive(self, message):
        # Check source argument
        if not message.get('source', None):
            raise MissingMessageKeyException('source')

        source = message['source']

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
                for article in parser_actor.ask({'source': source}):
                    yield article
            finally:
                # Stop actor
                parser_actor.stop()
        else:
            # If here, it means that sourcer is unknown
            raise UnknownSourcerException(sourcer)
