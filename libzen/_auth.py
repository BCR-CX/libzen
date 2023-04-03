import os


class AuthException(BaseException):
    pass


class _Authentication:
    authentication: '_Authentication'

    def __init__(self, url, name, secret) -> None:
        self._url = url
        self._name = name
        self._secret = secret

    @property
    def url(self) -> str:
        if not self._name:
            raise AuthException("Variável de ambiente ZENDESK_URL não definida")

        return self._url

    def to_tuple(self) -> tuple[str, str]:
        if not self._name:
            raise AuthException("Variável de ambiente ZENDESK_NAME não definida")

        if not self._secret:
            raise AuthException("Variável de ambiente ZENDESK_SECRET não definida")

        return (self._name, self._secret)

    @staticmethod
    def from_env():
        return _Authentication(
            os.getenv('ZENDESK_URL'),
            os.getenv('ZENDESK_NAME'),
            os.getenv('ZENDESK_SECRET'),
        )

    def __str__(self):
        return 'libzen._Authentication(omitted)'


def set_authentication(url, name, secret):
    _Authentication.authentication = _Authentication(url, name, secret)

_Authentication.authentication = _Authentication.from_env()
