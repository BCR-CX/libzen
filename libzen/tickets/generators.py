from libzen._generic import _iterate_search

def iterate_by_query(query: str):
    for tickets in _iterate_search('/api/v2/search?' + query):
        yield tickets
