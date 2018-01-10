'''
Created on 9 janv. 2018

@author: nribeiro
'''
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
        source = message['source']

        # Ask for sourcer articles
        sourcer_actor = ArticlesSourcerActor.start()
        articles = []
        for article in sourcer_actor.ask({'source': source}):
            articles.append(article)
            # Register article to iterator
            self.iterator.register(article)
        
        # Stop sourcer_actor
        sourcer_actor.stop()
        
        # Extract data for each article
        extracter_actors = set()
        for article in articles:
            extracter_actor = ArticleExtracterActor.start(self.iterator)
            extracter_actors.add(extracter_actor)
            extracter_actor.ask({'article': article},
                                block=False)

        # Return articles
        for article in self.iterator:
            yield article
        
        # Stop extracter_actors
        for actor in extracter_actors:
            actor.stop()
        