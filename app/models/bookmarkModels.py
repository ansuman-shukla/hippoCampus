def bookmarkModel(item):
    return {
        'id': str(item['_id']),
        'user_id': item['user_id'],
        'title': item['title'],
        'note': item['note'],
        'source_url': item['source_url'],
        'site_name': item['site_name'],
        'date': item['date']
    }

def bookmarkModels(items):
    return [bookmarkModel(item) for item in items]