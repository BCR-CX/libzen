from typing import Any
import json
import libzen
import requests

_METHOD = { 'post': requests.post, 'put': requests.put}

# TODO: fora, iterate_search, os outros metodos daqui não precisam ser geradores

def _send(endpoint:str, content_object:Any, result_page_name:str, headers=None, method:str='post'):
    """Função generica para enviar uma requisição com dados 'content_object' por um 'metodo' put/post para um 'endpoint' e retorna o contéudo 'result_page_name' do item devolvido pela requisição."""
    full_url = libzen._ZENDESK_URL + endpoint

    headers = headers or {'content-type': 'application/json'}
    response = _METHOD[method](full_url, data=content_object, auth=(libzen._ZENDESK_NAME, libzen._ZENDESK_SECRET), headers=headers)

    if response.status_code == 401: raise libzen.AuthException('Credenciais inválidas ou faltantes. Você setou as váriaveis de ambiente?')
    elif response.status_code > 299:
        err = json.loads(response.text.replace('\\', '\\\\'))
        msg = err.get('description', '')
        raise libzen.ZendeskException(msg, response.status_code, err)
    
    yield response.json()[result_page_name]


def _delete(endpoint: str, result_page_name: str='results'):
    full_url = libzen._ZENDESK_URL + endpoint

    response = requests.delete(full_url, auth=(libzen._ZENDESK_NAME, libzen._ZENDESK_SECRET))

    if response.status_code == 401: raise libzen.AuthException('Credenciais inválidas ou faltantes. Você setou as váriaveis de ambiente?')
    elif response.status_code > 299:
        err = json.loads(response.text.replace('\\', '\\\\'))
        msg = err.get('description', '')
        raise libzen.ZendeskException(msg, response.status_code, err)
    
    if 'application/json' in response.headers['content-type']:
        yield response.json().get(result_page_name)


def _iterate_search(endpoint: str, result_page_name: str='results'):
    """Gerador que obtém os resultados de 'endpoint' paginado de 100 em 100 e devolve o conteúdo de 'results' de cada iteração.
    NOTA: o gerador só retornará até 1000 resultados já que zendesk bloqueia com erro 'Unprocessed Entity' queries que tentam pegar mais que essa quantidade.
    """
    full_url = libzen._ZENDESK_URL + endpoint
    nextpage = full_url
    
    while True:
        response = requests.get(nextpage, auth=(libzen._ZENDESK_NAME, libzen._ZENDESK_SECRET))

        if response.status_code == 401: raise libzen.AuthException('Credenciais inválidas ou faltantes. Você setou as váriaveis de ambiente?')
        elif response.status_code == 422: break
        elif response.status_code > 299:
            err = json.loads(response.text.replace('\\', '\\\\'))
            msg = err.get('description', '')
            raise libzen.ZendeskException(msg, response.status_code, err)
        
        res_json  = response.json()

        yield res_json[result_page_name]

        nextpage = res_json['next_page']
        if nextpage is None:
            break
