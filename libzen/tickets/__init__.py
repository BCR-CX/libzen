from libzen._generic import _iterate_search, _delete, _post, _ZendeskException
from typing import Union, Optional
import json

_TICKET_VALID_FIELDS = set(['allow_attachments', 'allow_channelback', 'assignee_email', 'assignee_id', 'attribute_value_ids', 'brand_id', 'collaborator_ids', 'collaborators', 'comment', 'created_at', 'custom_fields', 'description', 'due_at', 'email_cc_ids', 'email_ccs', 'external_id', 'follower_ids', 'followers', 'followup_ids', 'forum_topic_id', 'group_id', 'has_incidents', 'id', 'is_public', 'macro_id', 'macro_ids', 'metadata', 'organization_id', 'priority', 'problem_id', 'raw_subject', 'recipient', 'requester', 'requester_id', 'safe_update', 'satisfaction_rating', 'sharing_agreement_ids', 'status', 'subject', 'submitter_id', 'tags', 'ticket_form_id', 'type', 'updated_at', 'updated_stamp', 'url', 'via', 'via_followup_source_id', 'via_id', 'voice_comment'])


def create(**ticket_fields) -> int:
    if not ticket_fields.get('description'):
        raise ValueError('422: campo description é obrigatorio')
    
    invalid_keys = set(ticket_fields.keys()).difference(_TICKET_VALID_FIELDS)
    if invalid_keys:
        raise ValueError(f"Chave {invalid_keys.pop()} não é um campo válido para um objeto de ticket.")

    data_ = json.dumps({ 'ticket': ticket_fields })
    return next(_post('/api/v2/tickets.json', data_, result_page_name='ticket'))['id']


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
    return next(_delete(endpoint, result_page_name='job_status'))['url']
