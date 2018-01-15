'''
Created on 2 janv. 2018

@author: tuco
'''

import logging
from time import mktime

import feedparser
import pykka

from core.newsparsing.sourcers import create_article
from core.newsparsing.sourcers.config.application import get_sources
from core.newsparsing.sourcers.config.rss import get_source_url
from core.newsparsing.sourcers.errors import MissingMessageKeyException, \
    UnknownSourceException, NoUrlException

logger = logging.getLogger('newsparsing.sourcers')


class FeedparserActor(pykka.ThreadingActor):

    def on_receive(self, message):
        if not message.get('source', None):
            raise MissingMessageKeyException('source')

        source = message['source']

        # Check source
        if source not in get_sources():
            raise UnknownSourceException(source)

        # Get url
        url = get_source_url(source)

        # Check url
        if not url:
            raise NoUrlException(source)

        # Get articles urls
        logger.debug('feedparser.parse %s' % url)
        rss_parsing = feedparser.parse(url)
        # Parse articles
        for rss_item in rss_parsing.entries:
            # Get article url
            article_url = rss_item.get('link', None)

            if article_url is not None:
                article = create_article(source,
                                         rss_item.get('guid', None))

                article['url'] = article_url
                if not rss_item.get('created_parsed', None) is None:
                    article['created'] = mktime(rss_item['created_parsed'])
                if not rss_item.get('published_parsed', None) is None:
                    article['published'] = mktime(rss_item['published_parsed'])
                if not rss_item.get('updated_parsed', None) is None:
                    article['updated'] = mktime(rss_item['updated_parsed'])
                if not rss_item.get('expired_parsed', None) is None:
                    article['expired'] = mktime(rss_item['expired_parsed'])
                # Yield article
                yield article
