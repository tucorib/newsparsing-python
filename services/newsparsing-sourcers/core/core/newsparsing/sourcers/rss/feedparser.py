'''
Created on 2 janv. 2018

@author: tuco
'''

import logging
from time import mktime

import feedparser

from core.newsparsing.sourcers import create_article
from core.newsparsing.sourcers.config.rss import get_rss_source_url
from core.newsparsing.sourcers.constants.source_type import RSS

logger = logging.getLogger('newsparsing.sourcers')


def get_feedparser_articles(source_name):
    # Get rss url
    rss_url = get_rss_source_url(source_name)
    # Get articles urls
    logger.debug('feedparser.parse %s' % rss_url)
    rss_parsing = feedparser.parse(rss_url)
    # Parse articles
    for rss_item in rss_parsing.entries:
        # Get article url
        article_url = rss_item.get('link', None)

        if article_url is not None:
            article = create_article(RSS,
                                     source_name,
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
            yield article
