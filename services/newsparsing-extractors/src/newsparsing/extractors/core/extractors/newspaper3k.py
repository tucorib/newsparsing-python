'''
Created on 2 janv. 2018

@author: tuco
'''
import logging

from newspaper.article import Article as NewspaperArticle
import pykka

from newsparsing.extractors.core.config.application import get_extractors_fields
from newsparsing.extractors.core.constants.extractors import NEWSPAPER3K
from newsparsing.extractors.core.errors import MissingMessageKeyException

logger = logging.getLogger('newsparsing.extractors')

ERROR_NO_URL = 'No url specified'


class Newspaper3kActor(pykka.ThreadingActor):

    def on_receive(self, message):
        # Check fields argument
        if not message.get('fields', None):
            raise MissingMessageKeyException('fields')
        # Check url argument
        if not message.get('url', None):
            raise MissingMessageKeyException('url')

        fields = message.get('fields')
        url = message.get('url')

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
