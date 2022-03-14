from libzen._generic import _iterate_search

def iterate_by_query(query: str):
    """Referência de pesquisa: https://developer.zendesk.com/api-reference/ticketing/ticket-management/search/"""
    for tickets in _iterate_search('/api/v2/search?' + query):
        yield tickets
