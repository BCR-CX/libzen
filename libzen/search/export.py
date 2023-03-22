from .._generic import _export_iterate_search


def iterate_by_query(query: str):
    if 'filter[type]=' not in query:
        raise ValueError('"filter[type]" é obrigatório na query')

    for tickets in _export_iterate_search('api/v2/search/export?' + query):
        yield tickets
