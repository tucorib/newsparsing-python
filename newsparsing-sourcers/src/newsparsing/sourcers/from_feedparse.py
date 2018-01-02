'''
Created on 2 janv. 2018

@author: tuco
'''
import feedparser
import datetime
from newsparsing.common.models.articles import ArticleDataBuilder


def get_articles(source_name, rss_source_url):
    # Get articles urls
    rss_parsing = feedparser.parse(rss_source_url)
    # Parse articles
    for rss_item in rss_parsing.entries:
        # Get article url
        article_url = rss_item.get('link', None)
        
        if not article_url is None:
            data_builder = ArticleDataBuilder(source_name, rss_item.get('guid', None))
            yield data_builder.build_data_from_content({
                'url': article_url,
                'sniffed': datetime.datetime.utcnow()
            })
