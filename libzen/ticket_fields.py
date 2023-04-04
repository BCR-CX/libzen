from ._generic import _iterate_search


def get_all() -> 'list[dict]':
    fields = []
    [fields.extend(items) for items in _iterate_search('/api/v2/ticket_fields', 'ticket_fields')]
    return fields
