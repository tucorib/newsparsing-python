'''
Created on 11 janv. 2018

@author: nribeiro
'''
import pykka

from core.newsparsing.extractors.config.application import get_extractors
from core.newsparsing.extractors.constants.extractors import NEWSPAPER3K
from core.newsparsing.extractors.errors import MissingMessageKeyException, \
    UnknownExtractorException
from core.newsparsing.extractors.extractors.newspaper3k import Newspaper3kActor


class ExtracterActor(pykka.ThreadingActor):

    def on_receive(self, message):
        # Check extractor argument
        if not message.get('extractor', None):
            raise MissingMessageKeyException('extractor')
        # Check fields argument
        if not message.get('fields', None):
            raise MissingMessageKeyException('fields')

        extractor = message.get('extractor')

        # Check extractor
        if extractor not in get_extractors():
            raise UnknownExtractorException(extractor)

        extracts = None

        if extractor == NEWSPAPER3K:
            # Start actor
            newspaper3k_actor = Newspaper3kActor.start()
            try:
                extracts = newspaper3k_actor.ask(message)
            finally:
                # Stop actor
                newspaper3k_actor.stop()

        return extracts
