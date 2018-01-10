'''
Created on 2 janv. 2018

@author: tuco
'''
from core.newsparsing.sourcers.config.application import get_configuration


def get_rss_source_url(rss_source):
    return get_configuration().get('sources.%s.url' % rss_source,
                                   None)

