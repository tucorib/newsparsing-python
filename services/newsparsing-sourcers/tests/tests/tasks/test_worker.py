'''
Created on 7 janv. 2018

@author: tuco
'''
import unittest

from tests.tasks import CeleryTestCase


class WorkerTestCase(unittest.TestCase, CeleryTestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        CeleryTestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def test_worker(self):
        worker = self.celery_app.Worker()
        self.assertTrue(worker)
