from ._generic import _iterate_search, _export_iterate_search

# Were using classes as namespace since if search was a folder
# (libzen/search/{__init__,export,generators}.py) will cause
# "cannot import name 'search' from partially initialized module" erros

class generators:
    @staticmethod
    def iterate_by_query(query: str):
        """Referência de pesquisa: 
        https://developer.zendesk.com/api-reference/ticketing/ticket-management/search
        """
        for tickets in _iterate_search('/api/v2/search?' + query):
            yield tickets


class export:
    @staticmethod
    def iterate_by_query(query: str):
        if 'filter[type]=' not in query:
            raise ValueError('"filter[type]" é obrigatório na query')

        for tickets in _export_iterate_search('api/v2/search/export?' + query):
            yield tickets


def get_by_query(query: str) -> 'list[dict]':
    all_results = []
    [all_results.extend(next_results) for next_results in generators.iterate_by_query(query)]
    return all_results
