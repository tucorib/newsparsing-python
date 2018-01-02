'''
Created on 2 janv. 2018

@author: tuco
'''
from newspaper.article import Article


def extract_article(article, fields):
    # Download article
    article = Article(url=article['content']['url'])
    article.download()
    # Parse article
    article.parse()
    
    extracts = {}
    if 'title' in fields:
        extracts['title'] = article.title
    if 'text' in fields:
        extracts['text'] = article.text
    if 'authors' in fields:
        extracts['authors'] = article.authors
    
    return extracts
