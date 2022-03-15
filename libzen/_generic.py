import libzen
import requests

class _ZendeskException(Exception):
    def __init__(self, msg:str, status_code:int):
        super().__init__(msg)
        self.status_code = status_code


def _delete(endpoint: str, result_page_name: str='results'):
    full_url = libzen._ZENDESK_URL + endpoint

    response = requests.delete(full_url, auth=(libzen._ZENDESK_NAME, libzen._ZENDESK_SECRET))

    if response.status_code == 401: raise libzen.AuthException('Credenciais inválidas ou faltantes. Você setou as váriaveis de ambiente?')
    elif response.status_code > 299:
        err = response.json()
        err = err.get('description', err.get('error', 'status code' + str(response.status_code)))
        raise _ZendeskException(err, response.status_code)
    
    yield response.json()[result_page_name]


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
            err = response.json()
            err = err.get('description', err.get('error', 'status code' + str(response.status_code)))
            raise _ZendeskException(err, response.status_code)
        
        res_json  = response.json()
        yield res_json[result_page_name]

        nextpage = res_json['next_page']
        if nextpage == None:
            break
