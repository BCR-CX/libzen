from ._generic import _iterate_search, _export_iterate_search

# Were using classes as namespace since if search was a folder
# (libzen/search/{__init__,export,generators}.py) will cause
# "cannot import name 'search' from partially initialized module" erros


def _prepare_query(query: str, sort_by: str = 'created_at', order_by: str = 'asc') -> dict:
    query = query.removeprefix('query=')
    return {'query': query, 'sort_by': sort_by, 'sort_order': order_by}


class generators:
    @staticmethod
    def iterate_by_query(query: str, sort_by: str='created_at', order_by: str='asc'):
        """Referência de pesquisa:
        https://developer.zendesk.com/api-reference/ticketing/ticket-management/search
        """
        params = _prepare_query(query, sort_by, order_by)
        for tickets in _iterate_search('/api/v2/search.json', params=params):
            yield tickets


class export:
    @staticmethod
    def iterate_by_query(query: str):
        if 'filter[type]=' not in query:
            raise ValueError('"filter[type]" é obrigatório na query')

        for tickets in _export_iterate_search('api/v2/search/export?' + query):
            yield tickets


def get_by_query(query: str, sort_by: str='created_at', order_by: str='asc') -> list[dict]:
    all_results = []

    for next_results in generators.iterate_by_query(query, sort_by, order_by):
        all_results.extend(next_results)

    return all_results
