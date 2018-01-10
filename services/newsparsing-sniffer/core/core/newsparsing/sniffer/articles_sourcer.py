'''
Created on 9 janv. 2018

@author: nribeiro
'''
from _io import BytesIO
import logging

import ijson
import pykka
import requests

from core.newsparsing.sniffer.config.application import get_service_sourcers

logger = logging.getLogger('newsparsing.sniffer')


class ArticlesSourcerActor(pykka.ThreadingActor):

    def on_receive(self, message):
        source = message['source']

        # Get articles from source
        logger.debug('Source articles from %s' % source)
        source_request = requests.get('%s/articles/%s' % (get_service_sourcers(),
                                                          source))
        # Return articles
        for article in ijson.items(BytesIO(source_request.content), 'item'):
            yield article
