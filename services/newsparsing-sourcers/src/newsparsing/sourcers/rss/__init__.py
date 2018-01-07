'''
Created on 6 janv. 2018

@author: tuco
'''
import feedparser
from newsparsing.sourcers import SourceType
from time import mktime
from newsparsing.sourcers.config.rss import get_rss_source_sourcer
from newsparsing.sourcers.rss.feedparser import get_feedparser_articles


def get_rss_articles(source_name):
    # Get sourcer
    sourcer = get_rss_source_sourcer(source_name)
    
    if sourcer == 'feedparser':
        for article in get_feedparser_articles(source_name):
            yield article
