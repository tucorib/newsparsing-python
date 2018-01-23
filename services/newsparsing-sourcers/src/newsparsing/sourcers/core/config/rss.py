'''
Created on 2 janv. 2018

@author: tuco
'''
from newsparsing.sourcers.core.config.application import get_configuration


def get_source_url(source):
    return get_configuration().get('sources.%s.url' % source,
                                   None)
