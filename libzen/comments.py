from typing import Union, Optional

from ._generic import _iterate_search
from .zendesk_exception import ZendeskException


def get(ticket_id: 'Union[str, int]') -> 'Optional[dict]':
    try:
        return next(_iterate_search(f"/api/v2/tickets/{ticket_id}/comments", result_page_name='comments'))
    except ZendeskException as ex:
        if ex.status_code == 404:
            return None

        raise ex
