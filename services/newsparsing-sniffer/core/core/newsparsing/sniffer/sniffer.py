'''
Created on 6 janv. 2018

@author: tuco
'''
from core.newsparsing.sniffer.articles_sniffer import ArticlesSnifferActor


def sniff(source_type, source_name):
    # Create async iterator
    articles_sniffer = ArticlesSnifferActor.start()
    for article in articles_sniffer.ask({'type': source_type,
                                         'name': source_name}):
        yield article
