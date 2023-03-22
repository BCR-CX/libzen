from typing import Union, Optional
import json
from .._generic import _iterate_search, _delete, _send
from .. import ZendeskException

_TICKET_VALID_FIELDS = set(['allow_attachments', 'allow_channelback', 'assignee_email',
                            'assignee_id', 'attribute_value_ids', 'brand_id',
                            'collaborator_ids', 'collaborators', 'comment', 'created_at',
                            'custom_fields', 'description', 'due_at', 'email_cc_ids',
                            'email_ccs', 'external_id', 'follower_ids', 'followers',
                            'followup_ids', 'forum_topic_id', 'group_id', 'has_incidents',
                            'id', 'is_public', 'macro_id', 'macro_ids', 'metadata',
                            'organization_id', 'priority', 'problem_id', 'raw_subject',
                            'recipient', 'requester', 'requester_id', 'safe_update',
                            'satisfaction_rating', 'sharing_agreement_ids', 'status',
                            'subject', 'submitter_id', 'tags', 'ticket_form_id', 'type',
                            'updated_at', 'updated_stamp', 'url',
                            'via', 'via_followup_source_id', 'via_id', 'voice_comment'])


def import_one(**ticket_props) -> int:
    import_valid_fields = _TICKET_VALID_FIELDS | set(['comments', 'archive_immediately'])
    invalid_keys = set(ticket_props.keys()) - import_valid_fields
    if invalid_keys:
        raise ValueError(f"Chave {invalid_keys.pop()} não é um campo válido para um objeto de ticket.")

    data = json.dumps({ 'ticket': ticket_props })
    return next(_send('/api/v2/imports/tickets', data, result_page_name='ticket', method='post'))['id']


def import_many(tickets:'list[dict]') -> str:
    if len(tickets) > 100:
        raise ValueError(f"Passados {len(tickets)}, esperado 100 ou menos.")

    data = json.dumps({ 'tickets': tickets})
    endpoint = '/api/v2/imports/tickets/create_many'
    return next(_send(endpoint, data, result_page_name='job_status', method='post'))['url']


def create(**ticket_props) -> int:
    if not ticket_props.get('description'):
        raise ValueError('422: campo description é obrigatorio')

    invalid_keys = set(ticket_props.keys()) - _TICKET_VALID_FIELDS
    if invalid_keys:
        raise ValueError(f"Chave {invalid_keys.pop()} não é um campo válido para um objeto de ticket.")

    data = json.dumps({ 'ticket': ticket_props })
    return next(_send('/api/v2/tickets.json', data, result_page_name='ticket', method='post'))['id']


def create_many(tickets:'list[dict]') -> str:
    if len(tickets) > 100:
        raise ValueError(f"Passados {len(tickets)}, esperado 100 ou menos.")

    data = json.dumps({ 'tickets': tickets})
    endpoint = '/api/v2/tickets/create_many'
    return next(_send(endpoint, data, result_page_name='job_status', method='post'))['url']


# TODO: mover essas checagens duplicadas para função aparte
def update(ticket_id:'Union[str, int]', **ticket_props) -> dict:
    invalid_keys = set(ticket_props.keys()) - _TICKET_VALID_FIELDS
    if invalid_keys:
        raise ValueError(f"Chave {invalid_keys.pop()} não é um campo válido para um objeto de ticket.")

    data = json.dumps({ 'ticket': ticket_props })
    return next(_send('/api/v2/tickets/' + str(ticket_id), data, result_page_name='ticket', method='put'))


def update_many(tickets:'list[dict]') -> str:
    """Dado uma lista de tickets, atualiza seus valores.
    NOTA: id é obrigatório"""

    if len(tickets) > 100:
        raise ValueError(f"Passados {len(tickets)}, esperado 100 ou menos.")
    elif len(tickets) == 0:
        raise ValueError("Nenhum id fornecido.")

    data = json.dumps({ 'tickets': tickets})
    endpoint = '/api/v2/tickets/update_many'
    return next(_send(endpoint, data, result_page_name='job_status', method='put'))['url']


def get_by_id(ticket_id:'Union[str, int]') -> 'Optional[dict]':
    try:
        return next(_iterate_search(f"/api/v2/tickets/{ticket_id}", result_page_name='ticket'))
    except ZendeskException as ex:
        if ex.status_code == 404:
            return None

        raise ex

def append_tags(ticket_id:'Union[str, int]', tags : 'list[str]') -> int:
    data = json.dumps({ 'tags': tags})
    headers = {'content-type': 'application/json'}
    return next(_send(f'/api/v2/tickets/{ticket_id}/tags', data, headers=headers, result_page_name='tags', method='put'))


def delete(ticket_id:'Union[str, int]'):
    endpoint = '/api/v2/tickets/' + str(ticket_id)
    _delete(endpoint, result_page_name='')


def delete_many(ids:'list[Union[str, int]]') -> str:
    if len(ids) > 100:
        raise ValueError(f"Passados {len(ids)}, esperado 100.")

    if len(ids) == 0:
        raise ValueError(f"Nenhum id fornecido.")

    ids_str = ','.join([str(id_) for id_ in ids])
    endpoint = '/api/v2/tickets/destroy_many?ids=' + ids_str
    return next(_delete(endpoint, result_page_name='job_status'))['url']
