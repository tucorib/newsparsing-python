'''
Created on 2 janv. 2018

@author: tuco
'''
from newspaper.article import Article as NewspaperArticle


def extract_fields(article, fields):
    # Download article
    newspaper_article = NewspaperArticle(url=article['content']['url'])
    newspaper_article.download()
    # Parse article
    newspaper_article.parse()
    
    extracts = {}
    if 'title' in fields:
        extracts['title'] = newspaper_article.title
    if 'text' in fields:
        extracts['text'] = newspaper_article.text
    if 'authors' in fields:
        extracts['authors'] = newspaper_article.authors
    return extracts