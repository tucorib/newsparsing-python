'''
Created on 11 janv. 2018

@author: tuco
'''


class MissingMessageKeyException(Exception):

    def __init__(self, key):
        Exception.__init__(self, 'Missing key %s' % key)


class UnknownSourceException(Exception):

    def __init__(self, source):
        Exception.__init__(self, 'Unknown source %s' % source)


class NoSourcerException(Exception):

    def __init__(self, source):
        Exception.__init__(self, 'Source %s has no sourcer' % source)


class NoUrlException(Exception):

    def __init__(self, source):
        Exception.__init__(self, 'Source %s has no url' % source)


class UnknownSourcerException(Exception):

    def __init__(self, source):
        Exception.__init__(self, 'Source %s has an unknown sourcer' % source)
