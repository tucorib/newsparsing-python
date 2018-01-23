from itertools import permutations
import os
from newsparsing.extractors.core.config.application import load_configuration


class ExtractorsTestCase():

    CONFIG_DIR = os.path.join(os.path.dirname(__file__), "../../conf")
    APPLICATION_CONFIGURATION = os.path.join(CONFIG_DIR,
                                             "tests.application.conf")

    def setUp(self):
        # Load configuration
        load_configuration(self.APPLICATION_CONFIGURATION)

    def get_fields_permutations(self):
        for nb_fields in range(len(self.get_expected_fields()) + 1):
                for fields_permutation in permutations(self.get_expected_fields(),
                                                       r=nb_fields):
                    yield fields_permutation

    def assertExtractedFields(self, fields, extracts):
        for field in fields:
            if not field in self.get_expected_fields():
                assert not field in extracts, 'Field %s should not be extracted' % field
