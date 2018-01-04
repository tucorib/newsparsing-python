'''
Created on 2 janv. 2018

@author: tuco
'''
from newsparsing.sniffer.sourcers import get_articles, get_source_extractors, \
    get_source_fields, get_source_field_extractors, get_source_extractor_fields
from newsparsing.sniffer.extractors import extract_fields


def sniff(source_type, source_name):
    # Get articles from sources
    for article in get_articles(source_type, source_name):
        # Extract data
        extracted_data = {}
        for extractor in get_source_extractors(source_type, source_name):
            extracted_data[extractor] = extract_fields(extractor, article, get_source_extractor_fields(source_type, source_name, extractor))
        # Set extracted data in article
        for field in get_source_fields(source_type, source_name):
            for extractor in get_source_field_extractors(source_type, source_name, field):
                for field in extracted_data[extractor]:
                    article.set_content(field, extracted_data[extractor][field])
                
        yield article