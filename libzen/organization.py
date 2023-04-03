import json
from typing import Union
from ._generic import _iterate_search, _send


_ORGS_VALID_FIELDS = set(['created_at', 'details', 'external_id', 'group_id', 'id', 'name', 'notes', 'organization_fields', 'shared_comments', 'shared_tickets', 'tags', 'updated_at', 'url'])


def create(**organization_props) -> int:
    if not organization_props.get('name'):
        raise ValueError('422: campo name é obrigatorio')
    
    invalid_keys = set(organization_props.keys()).difference(_ORGS_VALID_FIELDS)
    if invalid_keys:
        raise ValueError(f"Chave {invalid_keys.pop()} não é um campo válido para um objeto de ticket.")

    data = json.dumps({ 'organization': organization_props })
    return next(_send('/api/v2/organizations.json', data, result_page_name='organization', method='post'))['id']


# TODO: mover essas checagens duplicadas para função aparte
def update(organization_id:'Union[str, int]', **organization_props) -> dict:
    invalid_keys = set(organization_props.keys()).difference(_ORGS_VALID_FIELDS)
    if invalid_keys:
        raise ValueError(f"Chave {invalid_keys.pop()} não é um campo válido para um objeto de ticket.")

    data = json.dumps({ 'organization': organization_props })
    return next(_send('/api/v2/organizations/' + str(organization_id), data, result_page_name='organization', method='put'))


def get_all() -> 'list[dict]':
    orgs = []
    [orgs.extend(items) for items in _iterate_search('/api/v2/organizations', 'organizations')]
    return orgs
