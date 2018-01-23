from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import re
from threading import Thread
from unittest.mock import patch

from flask import json
import requests

from mock.article_service import start_articles_mock, stop_articles_mock
from mock.extractor_service import start_extractor_mock, stop_extractor_mock
from mock.sourcer_service import start_sourcer_mock, stop_sourcer_mock
from newsparsing.sniffer.core.config.application import load_configuration


def setUpModule():
    # Start mock services
    start_sourcer_mock()
    start_extractor_mock()
    start_articles_mock()


def tearDownModule():
    # Stop mock services
    stop_sourcer_mock()
    stop_extractor_mock()
    stop_articles_mock()


class CoreSnifferTestCase():

    CONFIG_DIR = os.path.join(os.path.dirname(__file__), "../../conf")
    APPLICATION_CONFIGURATION = os.path.join(CONFIG_DIR,
                                             "tests.application.conf")

    def get_api_headers(self):
        return {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def setUp(self):
        # Load configuration
        load_configuration(self.APPLICATION_CONFIGURATION)
