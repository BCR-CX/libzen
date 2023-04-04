from io import BufferedReader, TextIOWrapper
from pathlib import Path
from ._generic import _send


class InvalidReader(BaseException):
    pass


def create(fp: TextIOWrapper | BufferedReader, filename: str | None = None) -> 'tuple[str, int]':
    if fp.mode != 'rb':
        raise InvalidReader('Fp must be open in byte mode')

    if fp.closed:
        raise InvalidReader('Fp is closed')

    headers = {'Content-Type': 'application/binary'}
    filename = filename or Path(fp.name).name
    res = next(_send('api/v2/uploads?filename=' + filename, fp, 'upload', headers=headers))
    return res['token'], int(res['attachment']['id'])
