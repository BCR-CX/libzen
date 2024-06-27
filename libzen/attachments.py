from typing import TypeAlias
from io import BufferedReader, BytesIO, TextIOWrapper
from pathlib import Path
from ._generic import _send

_Type: TypeAlias = TextIOWrapper | BufferedReader | BytesIO


class InvalidReader(Exception):
    pass


def create(fp: _Type, filename: str | None = None) -> 'tuple[str, int]':
    # BytesIO não tem .mode
    if hasattr(fp, "mode") and fp.mode != 'rb':
        raise InvalidReader('Fp must be open in bytes mode')

    if fp.closed:
        raise InvalidReader('Fp is closed')

    headers = {'Content-Type': 'application/binary'}
    filename = filename or Path(fp.name).name
    res = next(_send('/api/v2/uploads?filename=' + filename, fp, 'upload', headers=headers))
    return res['token'], int(res['attachment']['id'])
