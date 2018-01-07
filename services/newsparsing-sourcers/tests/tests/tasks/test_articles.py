'''
Created on 7 janv. 2018

@author: tuco
'''
import unittest

from api.newsparsing.sourcers.celery_app import celery
from tests.tasks import CeleryTestCase


# Default task
@celery.task()
def returns(article):
    return article


class TasksTestCase(unittest.TestCase, CeleryTestCase):
    
    def setUp(self):
        unittest.TestCase.setUp(self)
        CeleryTestCase.setUp(self)
    
    def test_task_print_article(self):
        article = {'id': 'test'}
        res = returns.delay((article,))
        self.assertTrue(res.task_id)
        
        article_back = returns.wait()
        self.assertDictEqual(article_back, article, 'Task is wrong')
                    
