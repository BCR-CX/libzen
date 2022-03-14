import os

__author__ = 'BCR'

class AuthException(BaseException): pass

def _get_or_raise(var):
    if value := os.getenv(var):
        return value

    raise AuthException(f"Variável de ambiente '{var}' não definida")

# Not really secure to keep them stored
_ZENDESK_URL = _get_or_raise('ZENDESK_URL')
_ZENDESK_NAME = _get_or_raise('ZENDESK_NAME')
_ZENDESK_SECRET = _get_or_raise('ZENDESK_SECRET')
