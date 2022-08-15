from typing import Union, Optional

from libzen._generic import _iterate_search
import libzen


def get(ticket_id: 'Union[str, int]') -> 'Optional[dict]':
    try:
        return next(_iterate_search(f"/api/v2/tickets/{ticket_id}/comments", result_page_name='comments'))
    except libzen.ZendeskException as ex:
        if ex.status_code == 404:
            return None

        raise ex
