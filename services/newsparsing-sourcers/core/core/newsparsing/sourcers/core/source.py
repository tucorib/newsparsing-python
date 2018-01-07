'''
Created on 6 janv. 2018

@author: tuco
'''
import logging

from core.newsparsing.sourcers.core import SourceType
from core.newsparsing.sourcers.core.rss import get_rss_articles

logger = logging.getLogger('newsparsing.sourcers')


def get_articles(source_type, source_name):
    if source_type == SourceType.RSS:
        for article in get_rss_articles(source_name):
            logger.debug('article %s' % article['id'])
            yield article
