'''
Created on 16 janv. 2018

@author: nribeiro
'''


class MissingMessageKeyException(Exception):

    def __init__(self, key):
        Exception.__init__(self, 'Missing key %s' % key)


class UnknownExtractorException(Exception):

    def __init__(self, extractor):
        Exception.__init__(self, 'Unknown extractor %s' % extractor)
