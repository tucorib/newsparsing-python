'''
Created on 10 janv. 2018

@author: tuco
'''
from core.newsparsing.sourcers.articles import ArticlesActor


def get_articles(source):
    # Start actor
    articles_actor = ArticlesActor.start()
    for article in articles_actor.ask({'source': source}):
        yield article

    # Stop actor
    articles_actor.stop()
