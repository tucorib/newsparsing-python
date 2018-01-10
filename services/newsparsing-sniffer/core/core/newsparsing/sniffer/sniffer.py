'''
Created on 6 janv. 2018

@author: tuco
'''
from core.newsparsing.sniffer.articles_sniffer import ArticlesSnifferActor


def sniff(source):
    # Create async iterator
    articles_sniffer = ArticlesSnifferActor.start()
    for article in articles_sniffer.ask({'source': source}):
        yield article
    
    # Stop actor
    articles_sniffer.stop()
