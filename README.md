# libzen
  
Funções comuns para utilização da API da zendesk em importações

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
No linux: ``export ZENDESK_URL=valor``