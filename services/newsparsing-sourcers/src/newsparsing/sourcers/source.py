'''
Created on 6 janv. 2018

@author: tuco
'''
from newsparsing.sourcers import SourceType
from newsparsing.sourcers.rss import get_rss_articles


def get_articles(source_type, source_name):
    if source_type == SourceType.RSS:
        for article in get_rss_articles(source_name):
            yield article
