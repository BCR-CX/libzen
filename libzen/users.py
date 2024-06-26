import json
from ._generic import _send, _delete, _iterate_search
from .zendesk_exception import ZendeskException


_USER_VALID_FIELDS = set(
    [
        'id',
        'url',
        'name',
        'email',
        'created_at',
        'updated_at',
        'time_zone',
        'iana_time_zone',
        'phone',
        'shared_phone_number',
        'photo',
        'locale_id',
        'locale',
        'organization_id',
        'role',
        'verified',
        'external_id',
        'tags',
        'alias',
        'active',
        'shared',
        'shared_agent',
        'last_login_at',
        'two_factor_auth_enabled',
        'signature',
        'details',
        'notes',
        'role_type',
        'custom_role_id',
        'moderator',
        'ticket_restriction',
        'only_private_comments',
        'restricted_agent',
        'suspended',
        'default_group_id',
        'report_csv',
        'user_fields',
    ]
)


def create(**user_props) -> int:
    if not user_props.get('name'):
        raise ValueError('422: campo name é obrigatorio')

    invalid_keys = set(user_props.keys()) - _USER_VALID_FIELDS
    if invalid_keys:
        raise ValueError(f"Chave {invalid_keys.pop()} não é um campo válido para um objeto de usuário.")

    data = json.dumps({'user': user_props})

    return next(_send('/api/v2/users.json', data, result_page_name='user', method='post'))['id']


def update(user_id: str | int, **user_props) -> int:
    invalid_keys = set(user_props.keys()) - _USER_VALID_FIELDS
    if invalid_keys:
        raise ValueError(f"Chave {invalid_keys.pop()} não é um campo válido para um objeto de usuário.")

    data = json.dumps({'user': user_props})

    return next(_send(f"/api/v2/users/{user_id}", data, result_page_name="user", method="put"))


def create_many(users: 'list[dict]') -> str:
    if len(users) > 100:
        raise ValueError(f"Passados {len(users)}, esperado 100 ou menos.")

    data = json.dumps({'users': users})
    endpoint = '/api/v2/users/create_many'
    return next(_send(endpoint, data, result_page_name='job_status', method='post'))['url']


def delete(ticket_id: 'str | int'):
    endpoint = '/api/v2/users/' + str(ticket_id)
    return next(_delete(endpoint, result_page_name=''))


def get_by_id(user_id: 'Union[str, int]') -> 'Optional[dict]':
    try:
        return next(_iterate_search(f"/api/v2/users/{user_id}", result_page_name='user'))
    except ZendeskException as ex:
        if ex.status_code == 404:
            return None

        raise ex


def me() -> 'dict':
    return next(_iterate_search("/api/v2/users/me", result_page_name='user'))


def delete_many(ids: 'list[str | int]') -> str:
    if len(ids) > 100:
        raise ValueError(f"Passados {len(ids)}, esperado 100.")

    if len(ids) == 0:
        raise ValueError("Nenhum id fornecido.")

    ids_str = ','.join([str(id_) for id_ in ids])
    endpoint = '/api/v2/users/destroy_many?ids=' + ids_str
    return next(_delete(endpoint, result_page_name='job_status'))['url']
