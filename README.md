
  

## Instalação

Já que este pacote não está no PyPI é necessário clona-lo do repositório com o seguinte comando:

```python
git clone https://gitlab.com/dev-pos-vendas-bcr/python-libzen.git
pip install ./python-libzen
```

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

**libzen.tickets.create_many(tickets: list[dict]) -> str**  

Cria todos os tickets passados.  
Retorna uma string com a url da tarefa (job result)
```python
from libzen import tickets
print(tickets.create_many([
	{ 'subject': 'foo'},
	{ 'description': 'baz'}
]))
```

**libzen.tickets.get_by_id(ticket_id: str | int) -> Optional[dict]**  

Retorna o ticket de um dado id ou None caso ele não exista.
```python
from libzen import tickets
print(tickets.get_by_id(33435))
```

**libzen.tickets.update(ticket_id: str | int, \*\*ticket_props) -> dict**  

Semelhante a libzen.tickets.create, porém atualiza o ticket no lugar de criar.  
Retorna o ticket completo e atualizado  
```python
from libzen import tickets

ticket_id = tickets.update(1,  subject='suporte')

ticket = { 'description': 'foo'}
ticket_id = tickets.update(**ticket)
```

**libzen.tickets.update_many(tickets: list[dict] ) -> str**  

Atualiza todos os tickets que foram passados.  
Retorna uma string com a url da tarefa (job result)
```python
from libzen import tickets
print(tickets.update_many([
	{ 'id': 1, 'subject': 'foo'},
	{ 'id': 2, 'description': 'baz'}
]))
```

**libzen.tickets.append_tags(ticket_id: str | int, tags : list[str]) -> dict[str,str]**  

Adiciona tags ao ticket. Note que ele não sobrescreve as existentes. O retorno são todas as tags do ticket incluindo a que foi adicionada.    
```python
from libzen import tickets
tickets.append_tags(33435, ['tag1', 'tag2'])
```

**libzen.tickets.delete(ids: str | int)**  

Apaga o ticket com o id.    
```python
from libzen import tickets
tickets.delete(33435)
```

**libzen.tickets.delete_many(ids: list[str | int]) -> str**  

Apaga todos os tickets dos quais os ids foram passados como lista.    
Retorna uma string com a url da tarefa (job result)
```python
from libzen import tickets
print(tickets.get_by_id(33435))
```


**libzen.tickets.import_one(\*\*ticket_props) -> int**  

Semelhante a libzen.tickets.create, porém permite a adição de
comentários na criação do ticket e permite definir  uma flag
para arquivar imediatamente o ticket se o status dele é fechado.  
Retorna o ticket completo e atualizado  

Note que por esse endpoint o campo ``created_at`` não é de apenas
leitura. Mais informações [sobre o endpoint](https://developer.zendesk.com/api-reference/ticketing/tickets/ticket_import/#ticket-import).
```python
from libzen import tickets

comments = [
    {
        "created_at": "2009-06-25T10:15:18Z",
        "value": "I can upload"
    },
    {
        "public": False,
        "value": "multiple comments with it"
    }
]
ticket = { 'comments': comments }
ticket_id = tickets.import_one(**ticket, archive_immediately=True, status='closed')
```

**libzen.tickets.import_many(tickets: list[dict] ) -> str**  

Semelhante a libzen.tickets.import_one, porém permite cria multiplos
tickets. Retorna uma string com a url da tarefa (job result)
```python
from libzen import tickets

ticket_id = tickets.import_one(subject='suporte')

comments = [
    {
        "created_at": "2009-06-25T10:15:18Z",
        "value": "I can upload"
    },
    {
        "public": False,
        "value": "multiple comments with it"
    }
]

print(tickets.import_many([
	{ 'subject': 'foo'},
	{ 'comments': comments}
]))
```

### Ticket Comments

**libzen.comments.get(ticket_id: str | int) -> list[dict]**  

Retorna todos os comentário de um ticket.  
```python
from libzen import comments
comments = comments.get()
print(comments[0])
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


**libzen.search.export.iterate_by_query(query: str)**  

Itera sobre todos resultados de uma pesquisa no endpoint export. Para saber as
diferenças entre esse endpoint e o normal, leia a [documentação](https://developer.zendesk.com/api-reference/ticketing/ticket-management/search/#export-search-results).
```python
from libzen.search import export
for tickets in export.iterate_by_query('query=tags:teste&filter[type]=ticket'):
	print(tickets[0])
```

## Attachments

**libzen.attachments.create(fp: TextIOWrapper | BufferedReader, filename: str| None=None) -> tuple[str, int]**  

Cria um anexo e retorna uma tupla com o ``token`` e o id. O ``token`` é usado para anexa-lo em comentários de ticket.  
``fp`` é o arquivo a ser anexado, ele deve ser aberto em modo bytes. ``filename`` é o nome do arquivo após ser postado na zendesk, se não passado, ele será nomeado com o nome de ``fp``.
O arquivo passado como parâmetro deve ser aberto em modo de 'bytes'. Filename 
```python
from libzen import attachments, tickets
with open("./some-cool-image.png", 'rb') as file:
    token, id_ = attachments.create(file)
	
    tickets.update(1, comment={
        'body': 'here is a cool picture :^)',
        'uploads': [token]
    })

with open("./relatory.txt", 'rb') as file:
    token, id_ = attachments.create(file)
	tickets.update(1, comment={ 'body': 'You can see the relatory below.', 'uploads': [token] })	
```

### Organizations

**libzen.organizations.create(\*\*organization_props) -> int**  

Cria uma organização com os valores passados nos parâmetros nomeados (kwargs) como campos. Ele retorna o id da organização criado.  
NOTE: somente o nome é obrigatório.    
```python
from libzen import tickets

ticket_id = tickets.create(description='this is a description', subject='suporte')

ticket = { 'description': 'foo', 'requester_id': 0}
ticket_id = tickets.create(**ticket)
```

**libzen.organizations.update(organization_id: str | int, \*\*organization_props) -> dict**  

Semelhante a libzen.organizations.create, porém atualiza a organização no lugar de criar.  
Retorna a organização completa e atualizado  
```python
from libzen import organizations

org_id = organizations.update(1,  name='org name')

org = { 'description': 'foo'}
org_id = organizations.update(**org)
```

### Macros

**libzen.macros() -> list[dict]**  

Retorna todas as macros incluindo as desativadas.
```python
from libzen import macros
macros = macros.get_all()
print(macros[0])
```
