'''
Created on 11 janv. 2018

@author: tuco
'''


class MissingMessageKeyException(Exception):

    def __init__(self, key):
        Exception.__init__(self, 'Missing key %s' % key)
