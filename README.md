
  

## Instalação

Já que este pacote não está no PyPI é necessário dizer o caminho do repositório com o seguinte comando:

``pip install git+https://gitlab.com/dev-pos-vendas-bcr/python-libzen.git``

Em caso de desenvolvimento local, instale com o comando:

``pip3 install -e <caminho/local/para/o/repo>``

## Uso

É necessário definir as seguintes variáveis de ambiente para o programa:

* _ZENDESK_URL_: Endereço da zendesk com o subdomínio.  
* _ZENDESK_NAME_:  E-mail para login.  
* _ZENDESK_SECRET_: Senha para login.

Para criar variáveis de ambiente temporárias você pode usar os seguintes comandos:
No windows: ``set ZENDESK_URL=valor``
No *nix: ``export ZENDESK_URL=valor``

## Doc

### Search

``libzen.search.generators.iterate_by_query(query: str)``

Itera sobre todos resultados de uma pesquisa paginada.
```python
from libzen.search import generators
for tickets in generators.iterate_by_query('type:ticket status:closed'):
	print(tickets[0])
```

``libzen.search.get_by_query(query: str) -> list[dict]``  
Retorna todos resultados de uma pesquisa paginada.
```python
from libzen import search
tickets = search.get_by_query('type:ticket status:closed'):
print(tickets[0])
```
