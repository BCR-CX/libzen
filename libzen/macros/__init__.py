from libzen._generic import _iterate_search

def get_all() -> 'list[dict]':
    return next(_iterate_search('/api/v2/macros', 'macros'))
