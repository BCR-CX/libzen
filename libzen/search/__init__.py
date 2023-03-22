from ..search.generators import iterate_by_query
from . import export
from . import generators

def get_by_query(query: str) -> 'list[dict]':
    all_results = []
    [all_results.extend(next_results) for next_results in iterate_by_query(query)]
    return all_results
