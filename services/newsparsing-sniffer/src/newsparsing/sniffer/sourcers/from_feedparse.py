'''
Created on 2 janv. 2018

@author: tuco
'''
import feedparser
from newsparsing.sniffer.models.article import Article
from newsparsing.sniffer.sourcers import SourceType
from time import mktime


def get_articles(source_name, rss_source_url):
    # Get articles urls
    rss_parsing = feedparser.parse(rss_source_url)
    # Parse articles
    for rss_item in rss_parsing.entries:
        # Get article url
        article_url = rss_item.get('link', None)
        
        if not article_url is None:
            article = Article(SourceType.RSS, source_name, rss_item.get('guid', None))
            article.set_content('url', article_url)
            
            if not rss_item.get('created_parsed', None) is None:
                article.set_content('created', mktime(rss_item['created_parsed']))
            if not rss_item.get('published_parsed', None) is None:
                article.set_content('published', mktime(rss_item['published_parsed']))
            if not rss_item.get('updated_parsed', None) is None:
                article.set_content('updated', mktime(rss_item['updated_parsed']))
            if not rss_item.get('expired_parsed', None) is None:
                article.set_content('expired', mktime(rss_item['expired_parsed']))
            yield article
            