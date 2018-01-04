'''
Created on 2 janv. 2018

@author: tuco
'''


def get_article_id(rss_source_name, guid):
    return {
        'guid': guid,
        'source': {
            'name': rss_source_name,
            'type': 'rss'
        }
    }


def build_article(article, **kwargs):
    # Add attributes
    for k, v in kwargs.items():
        article['content'][k] = v
    return article
    
