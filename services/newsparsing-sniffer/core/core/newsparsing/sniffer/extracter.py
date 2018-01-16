'''
Created on 9 janv. 2018

@author: nribeiro
'''
import json
import logging

import pykka
import requests

from core.newsparsing.sniffer.config.application import get_source_fields, get_source_field_extractors, \
    get_service_extractors
from core.newsparsing.sniffer.constants.extractors import NEWSPAPER3K
from core.newsparsing.sniffer.errors import MissingMessageKeyException

logger = logging.getLogger('newsparsing.sniffer')


class ArticleExtracterActor(pykka.ThreadingActor):

    def __init__(self, parent, *args, **kwargs):
        pykka.ThreadingActor.__init__(self, *args, **kwargs)
        self.parent = parent

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
        self.parent.tell({'command': 'extract',
                          'id': article['id'],
                          'content': content})

    def __build_params(self, article, extractor, params):
        if extractor == NEWSPAPER3K:
            params['url'] = article['url']
