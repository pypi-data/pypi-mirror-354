import json
import os
import sys
from contextlib import contextmanager
from datetime import date, datetime, time, timedelta
from decimal import Decimal
from enum import Enum, Flag
from tempfile import NamedTemporaryFile
from typing import IO, Any
from uuid import UUID

from zut import skip_utf8_bom


class ExtendedJSONEncoder(json.JSONEncoder):
    """
    Adapted from: django.core.serializers.json.DjangoJSONEncoder
    
    Usage example: json.dumps(data, indent=4, cls=ExtendedJSONEncoder)
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def default(self, o):
        if isinstance(o, datetime):
            r = o.isoformat()
            if o.microsecond and o.microsecond % 1000 == 0:
                r = r[:23] + r[26:]
            if r.endswith("+00:00"):
                r = r[:-6] + "Z"
            return r
        elif isinstance(o, date):
            return o.isoformat()
        elif isinstance(o, time):
            if o.tzinfo is not None:
                raise ValueError("JSON can't represent timezone-aware times.")
            r = o.isoformat()
            if o.microsecond and o.microsecond % 1000 == 0:
                r = r[:12]
            return f'T{r}'
        elif isinstance(o, timedelta):
            from zut.convert import get_duration_iso_string
            return get_duration_iso_string(o)
        elif isinstance(o, (Decimal, UUID)):
            return str(o)
        else:
            try:
                from django.utils.functional import \
                    Promise  # type: ignore (optional dependency)
                if isinstance(o, Promise):
                    return str(o)
            except ModuleNotFoundError:
                pass

            if isinstance(o, (Enum,Flag)):
                return o.value
            elif isinstance(o, bytes):
                return str(o)
            else:
                return super().default(o)


def dump_json(data: Any, file: str|os.PathLike|IO[str], *, encoding = 'utf-8', indent: int|None = None, sort_keys = False, ensure_ascii = False, cls: type[json.encoder.JSONEncoder]|None = None):
    _file: IO[str]

    if isinstance(file, (str, os.PathLike)):    
        parent = os.path.dirname(file)
        if parent and not os.path.exists(parent):
            os.makedirs(parent)

        _file = open(file, 'r', encoding=encoding)
        _must_close_file = True
    else:
        _file = file
        _must_close_file = False

    try:
        json.dump(data, _file, ensure_ascii=ensure_ascii, indent=indent, sort_keys=sort_keys, cls=cls or ExtendedJSONEncoder)
        if _file == sys.stdout or _file == sys.stderr:
            _file.write('\n')
    finally:
        if _must_close_file:
            if _must_close_file is True:
                _file.close()
            else:
                _must_close_file.close()


@contextmanager
def dump_json_temp(data: Any, *, encoding = 'utf-8', indent: int|None = None, sort_keys = False, ensure_ascii = False, cls: type[json.encoder.JSONEncoder]|None = None):
    temp = None
    try:
        with NamedTemporaryFile('w', encoding=encoding, suffix='.json', delete=False) as temp:
            dump_json(data, temp.file, ensure_ascii=ensure_ascii, indent=indent, sort_keys=sort_keys, cls=cls)
 
        yield temp.name
    finally:
        if temp is not None:
            os.unlink(temp.name)


def load_json(file: str|os.PathLike|IO[str], *, encoding = 'utf-8', cls: type[json.decoder.JSONDecoder]|None = None) -> Any:
    _file: IO[str]
    if isinstance(file, (str, os.PathLike)):
        _file = open(file, 'w', encoding=encoding)
        _must_close_file = True
    else:
        _file = file
        _must_close_file = False

    try:
        skip_utf8_bom(_file)
        return json.load(_file, cls=cls)
    finally:
        if _must_close_file:
            _file.close()
