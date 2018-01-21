from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread
from unittest.mock import patch
import os
import re

from flask import json
import requests

from core.newsparsing.sniffer.config.application import load_configuration
from tests import CONFIG_DIR
from tests.mock.extractor_service import start_extractor_mock, \
    stop_extractor_mock
from tests.mock.sourcer_service import start_sourcer_mock, stop_sourcer_mock


class CoreSnifferTestCase():

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

    def setUpModule(self):
        # Start mock services
        start_sourcer_mock()
        start_extractor_mock()
    
    def tearDownModule(self):
        # Stop mock services
        stop_sourcer_mock()
        stop_extractor_mock()