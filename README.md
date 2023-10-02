[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=BCR-CX_libzen&metric=sqale_rating&token=311c784e0970b881bceae7cf1c4fc4859ebe7c1c)](https://sonarcloud.io/summary/new_code?id=BCR-CX_libzen)
[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=BCR-CX_libzen&metric=code_smells&token=311c784e0970b881bceae7cf1c4fc4859ebe7c1c)](https://sonarcloud.io/summary/new_code?id=BCR-CX_libzen)  
[![Lines of Code](https://sonarcloud.io/api/project_badges/measure?project=BCR-CX_libzen&metric=ncloc&token=311c784e0970b881bceae7cf1c4fc4859ebe7c1c)](https://sonarcloud.io/summary/new_code?id=BCR-CX_libzen)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=BCR-CX_libzen&metric=coverage&token=311c784e0970b881bceae7cf1c4fc4859ebe7c1c)](https://sonarcloud.io/summary/new_code?id=BCR-CX_libzen)
[![Technical Debt](https://sonarcloud.io/api/project_badges/measure?project=BCR-CX_libzen&metric=sqale_index&token=311c784e0970b881bceae7cf1c4fc4859ebe7c1c)](https://sonarcloud.io/summary/new_code?id=BCR-CX_libzen)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=BCR-CX_libzen&metric=alert_status&token=311c784e0970b881bceae7cf1c4fc4859ebe7c1c)](https://sonarcloud.io/summary/new_code?id=BCR-CX_libzen)
[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=BCR-CX_libzen&metric=reliability_rating&token=311c784e0970b881bceae7cf1c4fc4859ebe7c1c)](https://sonarcloud.io/summary/new_code?id=BCR-CX_libzen)
[![Duplicated Lines (%)](https://sonarcloud.io/api/project_badges/measure?project=BCR-CX_libzen&metric=duplicated_lines_density&token=311c784e0970b881bceae7cf1c4fc4859ebe7c1c)](https://sonarcloud.io/summary/new_code?id=BCR-CX_libzen)
[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=BCR-CX_libzen&metric=vulnerabilities&token=311c784e0970b881bceae7cf1c4fc4859ebe7c1c)](https://sonarcloud.io/summary/new_code?id=BCR-CX_libzen)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=BCR-CX_libzen&metric=bugs&token=311c784e0970b881bceae7cf1c4fc4859ebe7c1c)](https://sonarcloud.io/summary/new_code?id=BCR-CX_libzen)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=BCR-CX_libzen&metric=security_rating&token=311c784e0970b881bceae7cf1c4fc4859ebe7c1c)](https://sonarcloud.io/summary/new_code?id=BCR-CX_libzen)


## Instalação

Já que este pacote não está no PyPI é necessário clona-lo do repositório com o seguinte comando:

```python
git clone https://path.to.repo/python-libzen.git
pip install ./python-libzen
```

Use o argumento ``-e`` para que o pacote seja instalado em modo 'editável' para fins de desenvolvimento e debug. Isso pode
apresentar problemas no python 3.11 com o setuptools em uma versão menor que 58.3.0.

## Uso

Antes de começar a fazer as requisições é necessário definir as credenciais
e a url da zendesk que será acessada. Isso pode ser feito de duas formas:
via variáveis de ambiente ou via código.  

Caso seja necessário realizar a autentificação via token, adicione 
'/token' no final do email do usuário e coloque o token no lugar da
senha.  

Note que o pacote jogará um erro caso as credenciais não sejam definidas
antes de alguma função que realize requisições seja chamada.  

### Configurando autenticação por variáveis de ambiente 
Defina as seguintes variáveis de ambiente antes de executar o programa:

- **_ZENDESK_URL_**: Endereço da zendesk com o subdomínio.  
- **_ZENDESK_NAME_**:  E-mail para login. Acrecente '/token' no final caso deseje logar por token.  
- **_ZENDESK_SECRET_**: Senha ou token para login.

Para criar variáveis de ambiente locais no terminal atualmente aberto você pode usar os seguintes comandos:  
No windows: ``set VARIAVEL=valor``  
No *nix: ``export VARIAVEL=valor``  

### Configurando autenticação por código 

Caso prefira extrair as credenciais de outro lugar, você pode passa-las 
para a função ``set_authentication`` inves de definir as variáveis de ambiente.
```python
import libzen

email = ''

# Com autentificação básica
libzen.set_authentication('url', email, 'secret')

# Com token
libzen.set_authentication('url', email + '/token', 'token')

# Resto do código...
```

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
comments = comments.get(555443)
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

### Ticket Metrics

**libzen.ticket_fields.get_all(ticket_id: str | int) -> Optional[dict]**  

Retorna as metricas de um ticket de um dado id ou None caso ele o ticket não exista.  

```python
from libzen import metrics
ticket_metrics = metrics.get(66)
print(ticket_metrics)
```

### Users


**libzen.users.create(\*\*user_props) -> int**  

Cria um usuário com os valores passados nos parâmetros nomeados (kwargs) como campos. Ele retorna o id do usuário criado.  
NOTE: somente o name é obrigatório.
```python
from libzen import users

user_id = users.create(name='Jhon Doe', phone='555555555')

user = { 'name': 'foo', 'email': 'fo@baz.com'}
user_id = users.create(**user)
```

**libzen.users.create_many(users: list[dict]) -> str**  

Cria todos os usuários passados.  
Retorna uma string com a url da tarefa (job result)
```python
from libzen import users
print(users.create_many([
	{ 'name': 'foo', 'phone': '+000000'},
	{ 'name': 'baz', 'email': 'foo@baz.com'}
]))
```

**libzen.users.get_by_id(requester_id: str | int) -> Optional[dict]**  

Retorna o usuário de um dado id ou None caso ele não exista.
```python
from libzen import users
print(users.get_by_id(12345678))
```

**libzen.users.delete(ids: str | int)**  

Apaga o usuário com o id.  
```python
from libzen import users
users.delete(33435)
```

**libzen.users.delete_many(ids: list[str | int]) -> str**  

Apaga todos os usuários dos quais os ids foram passados como lista.  
Retorna uma string com a url da tarefa (job result)
```python
from libzen import users
print(users.get_by_id(33435))
```

### Search

**libzen.search.generators.iterate_by_query(query: str, sort_by: str='created_at', order_by: str='asc', timeout: int=60)**  

Itera sobre todos resultados de uma pesquisa paginada.
```python
from libzen.search import generators
for tickets in generators.iterate_by_query('type:ticket status:closed'):
	print(tickets[0])
```

**libzen.search.get_by_query(query: str, sort_by: str='created_at', order_by: str='asc', timeout: int=60) -> list[dict]**  

Retorna todos resultados de uma pesquisa paginada.
```python
from libzen import search
tickets = search.get_by_query('type:ticket status:closed', sort_by='created_at', sort_order='asc'):
print(tickets[0])
```


**libzen.search.export.iterate_by_query(query: str, timeout: int=60)**  

Itera sobre todos resultados de uma pesquisa no endpoint export. Para saber as
diferenças entre esse endpoint e o normal, leia a [documentação](https://developer.zendesk.com/api-reference/ticketing/ticket-management/search/#export-search-results).

Note: diferente dos outros search.get_by_query e search.generators.iterate_by_query, é
necessário prefixar com "query=".  
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

### Job Statuses

**libzen.wait_for_job(url: string, sleep_time=5) -> dict**  

Espera um job ser terminado e retorna o conteúdo. ``sleep_time`` é quanto vai esperar antes de tentar novamente.  

```python
from libzen import tickets, job_statuses
print(job_statuses.wait_for_job(tickets.create_many([
	{ 'subject': 'foo'},
	{ 'description': 'baz'}
])))
```
### Macros

**libzen.macros() -> list[dict]**  

Retorna todas as macros incluindo as desativadas.
```python
from libzen import macros
macros = macros.get_all()
print(macros[0])
```
