from test import ExtractorsTest
from newsparsing.extractors.newspaper3k import extract_fields
from itertools import permutations


class TestExtractor(ExtractorsTest):
    
    def get_expected_fields(self):
        []

    def get_test_url(self):
        return None
    
    def test_extract(self):
        if not self.get_test_url() is None:
            for nb_fields in range(len(self.get_expected_fields()) + 1):
                for fields_permutation in permutations(self.get_expected_fields(), r=nb_fields):
                    extracts = extract_fields(self.get_test_url(), fields_permutation)
                    
                    for field in self.get_expected_fields():
                        if not field in fields_permutation:
                            assert not field in extracts, 'Field %s should not be extracted' % field
