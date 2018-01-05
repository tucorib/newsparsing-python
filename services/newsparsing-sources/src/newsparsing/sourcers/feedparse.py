'''
Created on 2 janv. 2018

@author: tuco
'''
import feedparser
from newsparsing.sourcers import SourceType
from time import mktime
from newsparsing.sourcers.config.rss import get_rss_source_url


def get_articles(rss_source):
    # Get rss url
    rss_url = get_rss_source_url(rss_source)
    # Get articles urls
    rss_parsing = feedparser.parse(rss_url)
    # Parse articles
    for rss_item in rss_parsing.entries:
        # Get article url
        article_url = rss_item.get('link', None)
        
        if not article_url is None:
            article = {
                'source': {
                    'type': SourceType.RSS,
                    'name': rss_source
                },
                'id': rss_item.get('guid', None),
                'content': {
                    'url': article_url
                }
            }
            
            if not rss_item.get('created_parsed', None) is None:
                article['created'] = mktime(rss_item['created_parsed'])
            if not rss_item.get('published_parsed', None) is None:
                article['published'] = mktime(rss_item['published_parsed'])
            if not rss_item.get('updated_parsed', None) is None:
                article['updated'] = mktime(rss_item['updated_parsed'])
            if not rss_item.get('expired_parsed', None) is None:
                article['expired'] = mktime(rss_item['expired_parsed'])
            yield article
            