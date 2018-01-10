'''
Created on 9 janv. 2018

@author: nribeiro
'''
import json
import logging

import pykka
import requests

from core.newsparsing.sniffer.config.application import \
    get_service_extractors, get_source_fields, get_source_field_extractors
from core.newsparsing.sniffer.constants.extractors import NEWSPAPER3K

logger = logging.getLogger('newsparsing.sniffer')


class ArticleExtracterActor(pykka.ThreadingActor):

    def __init__(self, queue, *args, **kwargs):
        pykka.ThreadingActor.__init__(self, *args, **kwargs)
        self.queue = queue

    def on_receive(self, message):
        article = message['article']

        source_type = article['source']['type']
        source_name = article['source']['name']

        # Get fields to extract
        fields = get_source_fields(source_type, source_name)
        # Get extractors for source
        extractors = set()
        for field in fields:
            extractors = extractors.union(get_source_field_extractors(source_type,
                                                                      source_name,
                                                                      field))
        # Get extracts
        extracts = {}
        for extractor in extractors:
            # Request data
            params = {
                'extractor': extractor,
                'fields': fields
            }

            self.__build_params(article, extractor, params)

            # Request
            logger.debug('Extract article %s' % article['id'])
            extract_request = requests.post('%s/extract' % get_service_extractors(),
                                            data=json.dumps(params),
                                            headers={'Content-Type': 'application/json'})
            extracts[extractor] = extract_request.json()

        # Build content
        for field in fields:
            for extractor in get_source_field_extractors(source_type, source_name, field):
                article[field] = extracts[extractor][field]

        # Put extracts in queue
        self.queue.put(article)

    def __build_params(self, article, extractor, params):
        if extractor == NEWSPAPER3K:
            params['url'] = article['url']
