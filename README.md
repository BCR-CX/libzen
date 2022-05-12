
  

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

**libzen.tickets.create(\*\*ticket_props) -> int**  

Cria um ticket com os valores passados nos parâmetros nomeados (kwargs) como campos. Ele retorna o id do ticket criado.  
NOTE: somente a descrição é obrigatória, porém cada zendesk pode adicionar campos para serem obrigatórios.  
```python
from libzen import tickets

ticket_id = tickets.create(description='this is a description', subject='suporte')

ticket = { 'description': 'foo', 'requester_id': 0}
ticket_id = tickets.create(**ticket)
```

**libzen.tickets.create_many(tickets:'list[dict]') -> str**  

Cria todos os tickets passados.  
Retorna uma string com a url da tarefa (job result)
```python
from libzen import tickets
print(tickets.create_many([
	{ 'subject': 'foo'},
	{ 'description': 'baz'}
]))
```

**libzen.tickets.get_by_id(ticket_id:Union[str, int]) -> Optional[dict]**  

Retorna o ticket de um dado id ou None caso ele não exista.
```python
from libzen import tickets
print(tickets.get_by_id(33435))
```

**libzen.tickets.update(ticket_id:Union[str, int], **ticket_props) -> dict**  

Semelhante a libzen.tickets.create, porém atualiza o ticket no lugar de criar.  
Retorna o ticket completo e atualizado  
```python
from libzen import tickets

ticket_id = tickets.update(1,  subject='suporte')

ticket = { 'description': 'foo'}
ticket_id = tickets.update(**ticket)
```

**libzen.tickets.update_many(tickets:'list[dict]') -> str**  

Atualiza todos os tickets que foram passados.  
Retorna uma string com a url da tarefa (job result)
```python
from libzen import tickets
print(tickets.update_many([
	{ 'id': 1, 'subject': 'foo'},
	{ 'id': 2, 'description': 'baz'}
]))
```

**libzen.tickets.delete(ids:Union[str, int])**  

Apaga o ticket com o id.    
```python
from libzen import tickets
tickets.delete(33435)
```

**libzen.tickets.delete_many(ids:list[Union[str, int]]) -> str**  

Apaga todos os tickets dos quais os ids foram passados como lista.    
Retorna uma string com a url da tarefa (job result)
```python
from libzen import tickets
print(tickets.get_by_id(33435))
```

### Ticket Fields

**libzen.ticket_fields.get_all() -> list[dict]**  

Retorna todos os campos de ticket.
```python
from libzen import ticket_fields
fields = ticket_fields.get_all()
print(fields[0])
```

### Search

**libzen.search.generators.iterate_by_query(query: str)**  

Itera sobre todos resultados de uma pesquisa paginada.
```python
from libzen.search import generators
for tickets in generators.iterate_by_query('query=type:ticket status:closed'):
	print(tickets[0])
```

**libzen.search.get_by_query(query: str) -> list[dict]**  

Retorna todos resultados de uma pesquisa paginada.
```python
from libzen import search
tickets = search.get_by_query('query=type:ticket status:closed'):
print(tickets[0])
```

### Macros

**libzen.macros() -> list[dict]**  

Retorna todas as macros incluindo as desativadas.
```python
from libzen import macros
macros = macros.get_all()
print(macros[0])
```