'''
Created on 11 janv. 2018

@author: nribeiro
'''
import pykka

from core.newsparsing.extractors.config.application import get_extractors
from core.newsparsing.extractors.constants.extractors import NEWSPAPER3K
from core.newsparsing.extractors.extractors.newspaper3k import Newspaper3kActor

ERROR_UNKNOWN_EXTRACTOR = 'Unknwon extractor'


class ExtracterActor(pykka.ThreadingActor):

    def on_receive(self, message):
        extractor = message.get('extractor', None)
        fields = message.get('fields', None)

        # Check extractor
        if not extractor in get_extractors():
            return {'error': ERROR_UNKNOWN_EXTRACTOR}

        extracts = None

        if extractor == NEWSPAPER3K:
            # Start actor
            newspaper3k_actor = Newspaper3kActor.start()
            extracts = newspaper3k_actor.ask({'fields': fields, 'url': message.get('url', None)})
            # Stop actor
            newspaper3k_actor.stop()

        return extracts
