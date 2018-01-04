

class Extractor():
    NEWSPAPER_3K = 'newspaper3k'


def extract_fields(extractor, article, fields):
    if extractor == Extractor.NEWSPAPER_3K:
        from newsparsing.sniffer.extractors import from_newspaper3k
        from_newspaper3k.extract_fields(article, fields) 

    return article