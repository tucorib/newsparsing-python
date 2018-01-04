'''
Created on 2 janv. 2018

@author: tuco
'''
import feedparser
from newsparsing.sniffer.models.article import Article
from newsparsing.sniffer.sourcers import SourceType


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
            
            if 'published' in rss_item:
                article.set_content('published', rss_item['published'])
            yield article