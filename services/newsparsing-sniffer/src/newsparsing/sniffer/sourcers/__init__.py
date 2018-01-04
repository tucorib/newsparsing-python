import logging

logger = logging.getLogger('newsparsing.sourcers')


class SourceType():
    RSS = 'rss'


class Sourcer():
    FEEDPARSER = 'feedparser'


def get_articles(source_type, source_name):
    logger.debug('getting articles from %s, %s' % (source_type, source_name))
    if source_type == SourceType.RSS:
        from newsparsing.sniffer.sourcers.config.rss import get_rss_source_url, \
        get_rss_source_sourcer
        rss_url = get_rss_source_url(source_name)
        
        if rss_url:
            sourcer = get_rss_source_sourcer(source_name)
            
            if sourcer == Sourcer.FEEDPARSER:
                from newsparsing.sniffer.sourcers.from_feedparse import get_articles
                return get_articles(source_name, rss_url)

    return []


def get_source_extractors(source_type, source_name):
    if source_type == SourceType.RSS:
        from newsparsing.sniffer.sourcers.config.rss import get_rss_source_extractors
        return get_rss_source_extractors(source_name)
    
    return []

    
def get_source_fields(source_type, source_name):
    if source_type == SourceType.RSS:
        from newsparsing.sniffer.sourcers.config.rss import get_rss_source_fields
        return get_rss_source_fields(source_name)
    
    return []


def get_source_extractor_fields(source_type, source_name, extractor):
    if source_type == SourceType.RSS:
        from newsparsing.sniffer.sourcers.config.rss import get_rss_source_extractor_fields
        return get_rss_source_extractor_fields(source_name, extractor)
    
    return []


def get_source_field_extractors(source_type, source_name, field):
    if source_type == SourceType.RSS:
        from newsparsing.sniffer.sourcers.config.rss import get_rss_source_fields_extractors
        return get_rss_source_fields_extractors(source_name, field)
    
    return []


def get_source_database_name(source_type, source_name):
    if source_type == SourceType.RSS:
        from newsparsing.sniffer.sourcers.config.rss import get_rss_source_database_name
        return get_rss_source_database_name(source_name)
    
    return None


def get_source_database_url(source_type, source_name):
    if source_type == SourceType.RSS:
        from newsparsing.sniffer.sourcers.config.rss import get_rss_source_database_url
        return get_rss_source_database_url(source_name)
    
    return None
    
