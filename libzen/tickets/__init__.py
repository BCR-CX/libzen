from email.errors import FirstHeaderLineIsContinuationDefect
from xxlimited import foo
from libzen._generic import _iterate_search, _ZendeskException
from typing import Union, Optional


def get_by_id(ticket_id:'Union[str, int]') -> 'Optional[dict]':
    try:
        return next(_iterate_search(f"/api/v2/tickets/{ticket_id}", result_page_name='ticket'))
    except _ZendeskException as e:
        if e.status_code == 404:
            return None

        raise e
