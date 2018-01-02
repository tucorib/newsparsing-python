'''
Created on 2 janv. 2018

@author: tuco
'''
from newsparsing.sourcers import get_articles, get_source_extractors, \
    get_source_fields, get_source_field_extractors, get_source_extractor_fields
from newsparsing.extractors import extract_article
from newsparsing.articles.dao.sources import store_source
from newsparsing.articles.model.articles import build_article
from newsparsing.articles.dao.articles import store_article


def sniff(source_type, source_name):
    # Store source
    store_source(source_type, source_name)
    
    # Get articles from sources
    for article in get_articles(source_type, source_name):
        # Extract data
        extracted_data = {}
        for extractor in get_source_extractors(source_type, source_name):
            extracted_data[extractor] = extract_article(extractor, article, get_source_extractor_fields(source_type, source_name, extractor))
        # Set extracted data in article
        for field in get_source_fields(source_type, source_name):
            for extractor in get_source_field_extractors(source_type, source_name, field):
                build_article(article, **{field: extracted_data[extractor]})
                
        # Store article
        store_article(source_name, article)
