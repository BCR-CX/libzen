from ._generic import _iterate_search
from .zendesk_exception import ZendeskException


def get_all() -> 'list[dict]':
    fields = []
    [fields.extend(items) for items in _iterate_search('/api/v2/ticket_fields', 'ticket_fields')]
    return fields


def get(ticket_field_id: int):
    try:
        return next(
            _iterate_search(f"/api/v2/ticket_fields/{ticket_field_id}", result_page_name='ticket_field')
        )
    except ZendeskException as ex:
        if ex.status_code == 404:
            return None

        raise ex
