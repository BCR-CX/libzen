from ._generic import _iterate_search

# TODO: ta errado
def get_all() -> 'list[dict]':
    return next(_iterate_search('/api/v2/macros', 'macros'))
