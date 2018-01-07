'''
Created on 2 janv. 2018

@author: tuco
'''
from core.newsparsing.sourcers.core.config.application import get_configuration


def get_rss_sources():
    return get_configuration().get('sources.rss')


def get_rss_source_url(rss_source):
    return get_configuration().get('sources.rss.%s.url' % rss_source, None)


def get_rss_source_database_name(rss_source):
    return get_configuration().get('sources.rss.%s.storage.name' % rss_source, None)


def get_rss_source_database_url(rss_source):
    return get_configuration().get('sources.rss.%s.storage.url' % rss_source, None)


def get_rss_source_sourcer(rss_source):
    return get_configuration().get('sources.rss.%s.sourcer' % rss_source, None)
