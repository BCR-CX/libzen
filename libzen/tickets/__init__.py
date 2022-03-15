from libzen._generic import _iterate_search, _delete, _ZendeskException
from typing import Union, Optional


def get_by_id(ticket_id:'Union[str, int]') -> 'Optional[dict]':
    try:
        return next(_iterate_search(f"/api/v2/tickets/{ticket_id}", result_page_name='ticket'))
    except _ZendeskException as e:
        if e.status_code == 404:
            return None

        raise e


def delete_many(ids:'list[Union[str, int]]') -> str:
    if len(ids) > 100:
        raise ValueError(f"Passados {len(ids)}, esperado 100.")
    
    ids_str = ','.join([str(id_) for id_ in ids])
    endpoint = '/api/v2/tickets/destroy_many?ids=' + ids_str
    print(endpoint)
    return next(_delete(endpoint, result_page_name='job_status'))['url']
