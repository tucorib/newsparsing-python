def create_article(source_type, source_name, article_id):
    return {
        'source': {
            'type': source_type,
            'name': source_name
        },
        'id': article_id,
        'content': {}
    }
