
  

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

### Tickets

**libzen.tickets.create(\*\*ticket_fields) -> int**  

Cria um ticket com os valores passados nos parâmetros nomeados (kwargs) como campos. Ele retorna o id do ticket criado.  
NOTE: somente a descrição é obrigatória, porém cada zendesk pode adicionar campos para serem obrigatórios.  
```python
from libzen import tickets

ticket_id = tickets.create(description='this is a description', subject='suporte')

ticket = { 'description': 'foo', 'requester_id': 0}
ticket_id = tickets.create(**ticket)
```

**libzen.tickets.get_by_id(ticket_id:Union[str, int]) -> Optional[dict]**  

Retorna o ticket de um dado id ou None caso ele não exista.
```python
from libzen import tickets
print(tickets.get_by_id(33435))
```

**libzen.tickets.delete_many(ids:list[Union[str, int]]) -> str:**  

Apaga todos os tickets dos quais os ids foram passados como lista e retorna uma string com a url do job result para verificar o status da ação.
```python
from libzen import tickets
print(tickets.get_by_id(33435))
```

### Search

**libzen.search.generators.iterate_by_query(query: str)**  

Itera sobre todos resultados de uma pesquisa paginada.
```python
from libzen.search import generators
for tickets in generators.iterate_by_query('query=typetype:ticket status:closed'):
	print(tickets[0])
```

**libzen.search.get_by_query(query: str) -> list[dict]**  

Retorna todos resultados de uma pesquisa paginada.
```python
from libzen import search
tickets = search.get_by_query('query=typetype:ticket status:closed'):
print(tickets[0])
```
