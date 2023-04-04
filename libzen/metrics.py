from ._generic import _iterate_search
from .zendesk_exception import ZendeskException


def get(ticket_id):
    try:
        return next(
            _iterate_search(f"/api/v2/tickets/{ticket_id}/metrics", result_page_name='ticket_metric')
        )
    except ZendeskException as ex:
        if ex.status_code == 404:
            return None

        raise ex
