'''
Created on 2 janv. 2018

@author: tuco
'''
from newsparsing.common.configuration import get_configuration

SOURCE_RSS_DEFAULT = 'default'


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


def get_rss_source_extractors(rss_source):
    extractors = set()
    for field in get_rss_source_fields(rss_source):
        extractors = extractors.union(get_rss_source_fields_extractors(rss_source, field))
            
    return extractors


def get_rss_source_fields(rss_source):
    return get_configuration().get('sources.rss.%s.fields' % rss_source, {}).keys()


def get_rss_source_extractor_fields(rss_source, extractor):
    return [field for field in get_rss_source_fields(rss_source) if extractor in get_rss_source_fields_extractors(rss_source, field)]


def get_rss_source_fields_extractors(rss_source, field):
    return get_configuration().get('sources.rss.%s.fields.%s.extractors' % (rss_source, field), [])
