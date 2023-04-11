from typing import Any
import json
import requests
from ._auth import _Authentication, AuthException
from .zendesk_exception import ZendeskException


_METHOD = {'post': requests.post, 'put': requests.put}

# TODO: fora, iterate_search, os outros metodos daqui não precisam ser geradores


def _send(endpoint: str, content_object: Any, result_page_name: str, headers=None, method: str = 'post'):
    """Função generica para enviar uma requisição com dados 'content_object' por um 'metodo' put/post para um 'endpoint' e retorna o contéudo 'result_page_name' do item devolvido pela requisição."""
    full_url = _Authentication.authentication.url + endpoint

    headers = headers or {'content-type': 'application/json'}
    response = _METHOD[method](
        full_url, data=content_object, auth=_Authentication.authentication.to_tuple(), headers=headers
    )

    if response.status_code == 401:
        raise AuthException('Credenciais inválidas ou faltantes. Você setou as váriaveis de ambiente?')
    elif response.status_code > 299:
        err = json.loads(response.text.replace('\\', '\\\\'))
        msg = err.get('description', '')
        raise ZendeskException(msg, response.status_code, err, dict(response.headers))

    yield response.json()[result_page_name]


def _delete(endpoint: str, result_page_name: str = 'results'):
    full_url = _Authentication.authentication.url + endpoint

    response = requests.delete(full_url, auth=_Authentication.authentication.to_tuple(), timeout=2)
    if response.status_code == 401:
        raise AuthException('Credenciais inválidas ou faltantes. Você setou as váriaveis de ambiente?')
    elif response.status_code > 299:
        err = json.loads(response.text.replace('\\', '\\\\'))
        msg = err.get('description', '')
        raise ZendeskException(msg, response.status_code, err, dict(response.headers))

    if 'application/json' in response.headers.get('content-type', {}):
        yield response.json().get(result_page_name)
    else:
        yield {}


def _iterate_search(endpoint: str, result_page_name: str = 'results'):
    """Gerador que obtém os resultados de 'endpoint' paginado de 100 em 100 e devolve o conteúdo de 'results' de cada iteração.
    NOTA: o gerador só retornará até 1000 resultados já que zendesk bloqueia com erro 'Unprocessed Entity' queries que tentam pegar mais que essa quantidade.
    """
    full_url = _Authentication.authentication.url + endpoint
    nextpage = full_url

    while True:
        response = requests.get(nextpage, auth=_Authentication.authentication.to_tuple(), timeout=2)

        if response.status_code == 401:
            raise AuthException(
                'Credenciais inválidas ou faltantes. Você setou as váriaveis de ambiente?'
            )
        elif response.status_code == 422:
            break
        elif response.status_code > 299:
            msg = ''
            err = {}
            if response.headers.get('Content-Type') == 'application/json':
                err = json.loads(response.text.replace('\\', '\\\\'))
                msg = err.get('description', '')
            raise ZendeskException(msg, response.status_code, err, dict(response.headers))

        res_json = response.json()

        yield res_json[result_page_name]

        nextpage = res_json['next_page']
        if nextpage is None:
            break


def _export_iterate_search(endpoint: str, result_page_name: str = 'results'):
    full_url = _Authentication.authentication.url + endpoint
    nextpage = full_url

    while True:
        response = requests.get(nextpage, auth=_Authentication.authentication.to_tuple(), timeout=2)

        if response.status_code == 401:
            raise AuthException(
                'Credenciais inválidas ou faltantes. Você setou as váriaveis de ambiente?'
            )
        elif response.status_code == 422:
            break
        elif response.status_code > 299:
            err = json.loads(response.text.replace('\\', '\\\\'))
            msg = err.get('description', '')
            raise ZendeskException(msg, response.status_code, err, dict(response.headers))

        res_json = response.json()

        yield res_json[result_page_name]

        # Unicas linhas diferentes em relação a _iterate_search
        nextpage = res_json['links']['next']
        if not res_json['meta']['has_more']:
            break
