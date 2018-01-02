

class Extractor():
    NEWSPAPER_3K = 'newspaper3k'


def extract_article(extractor, article, fields):
    if extractor == Extractor.NEWSPAPER_3K:
        from newsparsing.extractors import from_newspaper3k
        return from_newspaper3k.extract_article(article, fields) 

    return article