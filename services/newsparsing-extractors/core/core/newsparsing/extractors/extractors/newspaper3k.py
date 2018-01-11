'''
Created on 2 janv. 2018

@author: tuco
'''
import logging

from newspaper.article import Article as NewspaperArticle
import pykka

from core.newsparsing.extractors.config.application import get_extractors_fields
from core.newsparsing.extractors.constants.extractors import NEWSPAPER3K

logger = logging.getLogger('newsparsing.extractors')

ERROR_NO_URL = 'No url specified'


class Newspaper3kActor(pykka.ThreadingActor):

    def on_receive(self, message):
        fields = message.get('fields', None)
        url = message.get('url', None)

        # Check extractor
        if url is None:
            return {'error': ERROR_NO_URL}

        logger.debug('[%s] Extracting %s from %s' % (NEWSPAPER3K,
                                                 ', '.join(fields),
                                                 url))
        # Download article
        newspaper_article = NewspaperArticle(url=url)
        newspaper_article.download()
        # Parse article
        newspaper_article.parse()

        extracts = {}
        for field in fields:
            if field in get_extractors_fields(NEWSPAPER3K):
                if field == 'url':
                    extracts['url'] = url
                if field == 'title':
                    extracts['title'] = newspaper_article.title
                if field == 'text':
                    extracts['text'] = newspaper_article.text
                if field == 'authors':
                    extracts['authors'] = newspaper_article.authors
        return extracts
