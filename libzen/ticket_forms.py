"""Busca as informações de formulários de tickets."""
from libzen._generic import _iterate_search
from libzen.zendesk_exception import ZendeskException


def get_all() -> 'list[dict]':
    ticket_forms = []
    [ticket_forms.extend(items) for items in _iterate_search('/api/v2/ticket_forms', 'ticket_forms')]
    return ticket_forms


def get(ticket_form_id: int):
    try:
        return next(
            _iterate_search(f"/api/v2/ticket_forms/{ticket_form_id}", result_page_name='ticket_form')
        )
    except ZendeskException as ex:
        if ex.status_code == 404:
            return None

        raise ex
