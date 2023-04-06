"""Teste inicial para validação do processo de CI"""
from libzen._generic import _METHOD
import pytest


@pytest.mark.parametrize(
    'method, expected', [
        ('get', False),
        ('post', True),
        ('put', True),
        ('delete', False),
    ])
def test_method_props(method, expected):
    """Testa se os métodos HTTP estão definidos corretamente"""
    result = method in set(_METHOD.keys())

    assert result == expected
