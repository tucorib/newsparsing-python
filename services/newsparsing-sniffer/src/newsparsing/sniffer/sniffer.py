'''
Created on 6 janv. 2018

@author: tuco
'''
import requests
from newsparsing.sniffer.config.application import get_source_fields, get_source_field_extractors, get_service_sourcers, get_service_extractors 
from flask import json
import ijson
from _io import BytesIO


def sniff(source_type, source_name):
    # Get extractors and related fields
    extractors = {}
    for field in get_source_fields(source_type, source_name):
        for extractor in get_source_field_extractors(source_type, source_name, field):
            if not extractor in extractors:
                extractors[extractor] = set()
            extractors[extractor].add(field)
        
    # Get articles from source
    source_request = requests.get('%s/articles/%s/%s' % (get_service_sourcers(),
                                                         source_type,
                                                         source_name))
    
    for article in ijson.items(BytesIO(source_request.content), 'item'):
        # Get extracts
        article_extracts = {}
        for extractor in extractors:
            # Request data
            params = {
                'extractor': extractor,
                'fields': list(extractors[extractor])
            }
            
            if extractor == 'newspaper3k':
                params['url'] = article['content']['url']
            
            # Request    
            extract_request = requests.post('%s/extract' % get_service_extractors(),
                                            data=json.dumps(params),
                                            headers={'Content-Type': 'application/json'})
            article_extracts[extractor] = extract_request.json()
        
        # Build content
        for field in get_source_fields(source_type, source_name):
            for extractor in get_source_field_extractors(source_type, source_name, field):
                article['content'][field] = article_extracts[extractor][field]

        # Return article
        yield article
        