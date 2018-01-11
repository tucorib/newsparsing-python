'''
Created on 11 janv. 2018

@author: nribeiro
'''
import pykka

from core.newsparsing.sourcers.config.application import get_source_sourcer
from core.newsparsing.sourcers.sourcers.feedparser import FeedparserActor


class ArticlesActor(pykka.ThreadingActor):

    def on_receive(self, message):
        source = message['source']

        # Get sourcer
        sourcer = get_source_sourcer(source)

        if sourcer == 'feedparser':
            # Start actor
            feedparsor_actor = FeedparserActor.start()
            for article in feedparsor_actor.ask({'source': source}):
                yield article

            # Stop actor
            feedparsor_actor.stop()
