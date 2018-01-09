'''
Created on 7 janv. 2018

@author: tuco
'''
import unittest
from api.newsparsing.extractors.celery_app import celery
from tests.tasks import CeleryTestCase


# Test task
@celery.task
def returns(data):
    return data


class BrokerTestCase(unittest.TestCase, CeleryTestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        CeleryTestCase.setUp(self)

    def test_task(self):
        # Check task is registred
        self.assertIn(returns.name,
                      self.celery_app.tasks,
                      'Task is not registred')

        # Define chain
        data = 'Test'
        chain = returns.s(data)

        # Launch chain
        data_back = chain()
        self.assertEqual(data_back,
                         data,
                         'Task result is wrong')
