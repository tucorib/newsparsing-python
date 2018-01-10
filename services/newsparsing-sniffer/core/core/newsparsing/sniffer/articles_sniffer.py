'''
Created on 9 janv. 2018

@author: nribeiro
'''
import logging
from queue import Queue

import pykka

from core.newsparsing.sniffer.article_extracter import ArticleExtracterActor
from core.newsparsing.sniffer.articles_sourcer import ArticlesSourcerActor


class ArticlesIterator:

    pendings = set()
    readys = Queue()

    def register(self, article):
        self.pendings.add(article['id'])

    def put(self, article):
        self.pendings.remove(article['id'])
        self.readys.put(article)

    def __iter__(self):
        return self

    def __next__(self):
        # Raise stop iteration if no article pending
        if len(self.pendings) == 0:
            raise StopIteration

        # Pop a ready article
        return self.readys.get()


class ArticlesSnifferActor(pykka.ThreadingActor):

    def on_receive(self, message):
        # Create async itreator
        self.iterator = ArticlesIterator()

        # Get params
        self.source_type = message['type']
        self.source_name = message['name']

        # Ask for sourcer articles
        sourcer_actor = ArticlesSourcerActor.start()
        for article in sourcer_actor.ask({'type': self.source_type,
                                          'name': self.source_name}):
            # Register article to iterator
            self.iterator.register(article)
            # Extract data for each article
            extracter_actor = ArticleExtracterActor.start(self.iterator)
            extracter_actor.ask({'article': article},
                                block=False)

        # Yield iterator data
        for article in self.iterator:
            yield article
