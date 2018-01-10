'''
Created on 10 janv. 2018

@author: tuco
'''
from core.newsparsing.sourcers.config.application import get_source_sourcer
from core.newsparsing.sourcers.sourcers.feedparser import get_feedparser_articles


def get_articles(source):
    # Get sourcer
    sourcer = get_source_sourcer(source)

    if sourcer == 'feedparser':
        for article in get_feedparser_articles(source):
            yield article
