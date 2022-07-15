import os

__author__ = 'BCR'

class AuthException(BaseException): pass


class ZendeskException(Exception):
    def __init__(self, msg:str, status_code:int, details:dict):
        super().__init__(msg)
        self.status_code = status_code
        self.details = details
    
    def __str__(self):
        return f"{super().__str__()} | {self.status_code} | {str(self.details)}"


def _get_or_raise(var):
    if value := os.getenv(var):
        return value

    raise AuthException(f"Variável de ambiente '{var}' não definida")

# Not really secure to keep them stored
_ZENDESK_URL = _get_or_raise('ZENDESK_URL')
_ZENDESK_NAME = _get_or_raise('ZENDESK_NAME')
_ZENDESK_SECRET = _get_or_raise('ZENDESK_SECRET')
