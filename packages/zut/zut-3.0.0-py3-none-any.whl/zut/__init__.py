"""
Reusable Python utilities.
"""
from __future__ import annotations

import logging
import os
import re
import sys
import unicodedata
from contextlib import contextmanager
from getpass import getuser
from io import UnsupportedOperation
from pathlib import Path
from tempfile import mktemp
from typing import IO, Protocol, TypeVar, runtime_checkable
from warnings import catch_warnings

__prog__ = 'zut'

__version__: str
__version_tuple__: tuple[int|str, ...]
try:
    from ._version import __version__, __version_tuple__  # type: ignore
except ModuleNotFoundError:
    __version__ = '?'
    __version_tuple__ = (1_000_000_000, 0, 0, '?')


T = TypeVar('T')


#region Text

def slugify(value: str, *, separator: str|None = '-', keep: str|None = '_', as_separator: str|None = None, strip_separator: bool = True, strip_keep: bool = True, if_none: str|None = 'none', additional_conversions: dict[str,str]|None = None) -> str:
    """ 
    Generate a slug.

    Difference between `keep` and `as_separator`
    - `keep`: these characters are kept as is in the resulting slug
    - `as_separator`: these characters are transformed to a separator before the operation

    Identical to `django.utils.text.slugify` if no options are given.
    """
    if value is None:
        return if_none
    
    separator = separator if separator is not None else ''
    keep = keep if keep is not None else ''

    if as_separator:
        value = re.sub(f"[{re.escape(as_separator)}]", separator, value)

    # Normalize the string: replace diacritics by standard characters, lower the string, etc
    value = str(value)
    if additional_conversions:
        converted_value = ''
        for char in value:
            converted_char = additional_conversions.get(char)
            if converted_char is None:
                converted_char = char
            converted_value += converted_char
        value = converted_value
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    value = value.lower()

    # Remove special characters
    remove_sequence = r'^a-zA-Z0-9\s' + re.escape(separator) + re.escape(keep)
    value = re.sub(f"[{remove_sequence}]", "", value)

    # Replace spaces and successive separators by a single separator
    replace_sequence = r'\s' + re.escape(separator)
    value = re.sub(f"[{replace_sequence}]+", separator, value)
    
    # Strips separator and kept characters
    strip_chars = (separator if strip_separator else '') + (keep if strip_keep else '')
    value = value.strip(strip_chars)

    return value


def slugify_snake(value: str, separator: str|None = '_', if_none: str|None = 'none', additional_conversions: dict[str,str]|None = None) -> str:
    """
    CamèlCase => camel_case
    """
    if value is None:
        return if_none
    
    separator = separator if separator is not None else ''
    
    # Normalize the string: replace diacritics by standard characters, etc
    # NOTE: don't lower the string
    value = str(value)
    if additional_conversions:
        converted_value = ''
        for char in value:
            converted_char = additional_conversions.get(char)
            if converted_char is None:
                converted_char = char
            converted_value += converted_char
        value = converted_value
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    
    value = re.sub(r"[^\w\s-]", "", value)
    value = re.sub(r"[-_\s]+", separator, value).strip(separator)
    value = re.sub(r'(.)([A-Z][a-z]+)', f'\\1{separator}\\2', value)
    return re.sub(r'([a-z0-9])([A-Z])', f'\\1{separator}\\2', value).lower()


def slugen(value: str, separator: str|None = '-', keep: str|None = None) -> str:
    """
    Similar as `slugify` except than some defaults are changed compared to Django's version and some additional letters are handled.
    Closer to Postgres' unaccent result.
    """
    #Input examples that give different results than `slugify`: `AN_INPUT`, `Ørland`
    if value is None:
        return value
    
    value = value.replace('_', '-')
    
    return slugify(value, separator=separator, keep=keep, if_none=None, additional_conversions={ # non-ASCII letters that are not separated by "NFKD" normalization
        "œ": "oe",
        "Œ": "OE",
        "ø": "o",
        "Ø": "O",
        "æ": "ae",
        "Æ": "AE",
        "ß": "ss",
        "ẞ": "SS",
        "đ": "d",
        "Đ": "D",
        "ð": "d",
        "Ð": "D",
        "þ": "th",
        "Þ": "th",
        "ł": "l",
        "Ł": "L",
        "´": "", # in order to have same result as for "'"
    })


def skip_utf8_bom(fp: IO, encoding: str|None = None):
    """
    Skip UTF8 byte order mark, if any.
    - `fp`: opened file pointer.
    - `encoding`: if given, do nothing unless encoding is utf-8 or alike.
    """
    if encoding and not encoding in {'utf8', 'utf-8', 'utf-8-sig'}:
        return False

    try:
        start_pos = fp.tell()
    except UnsupportedOperation: # e.g. empty file
        start_pos = 0

    try:
        data = fp.read(1)
    except UnsupportedOperation: # e.g. empty file
        return False
    
    if isinstance(data, str): # text mode
        if len(data) >= 1 and data[0] == UTF8_BOM:
            return True
        
    elif isinstance(data, bytes): # binary mode
        if len(data) >= 1 and data[0] == UTF8_BOM_BINARY[0]:
            data += fp.read(2) # type: ignore (data bytes => fp reads bytes)
            if data[0:3] == UTF8_BOM_BINARY:
                return True
    
    fp.seek(start_pos)
    return False


def fix_utf8_surrogateescape(text: str, potential_encoding = 'cp1252') -> tuple[str,bool]:
    """ Fix potential encoding issues for files open with `file.open('r', encoding='utf-8', errors='surrogateescape')`. """
    fixed = False
    for c in text:
        c_ord = ord(c)
        if c_ord >= SURROGATE_MIN_ORD and c_ord <= SURROGATE_MAX_ORD:
            fixed = True
            break

    if not fixed:
        return text, False
    
    return text.encode('utf-8', 'surrogateescape').decode(potential_encoding, 'replace'), fixed


def fix_restricted_xml_control_characters(text: str, replace = '?'):
    """
    Replace invalid XML control characters. See: https://www.w3.org/TR/xml11/#charsets.
    """
    if text is None:
        return None
    
    replaced_line = ''
    for c in text:
        n = ord(c)
        if (n >= 0x01 and n <= 0x08) or (n >= 0x0B and n <= 0x0C) or (n >= 0x0E and n <= 0x1F) or (n >= 0x7F and n <= 0x84) or (n >= 0x86 and n <= 0x9F):
            c = replace
        replaced_line += c
    return replaced_line


UTF8_BOM = '\ufeff'
UTF8_BOM_BINARY = UTF8_BOM.encode('utf-8')

SURROGATE_MIN_ORD = ord('\uDC80')
SURROGATE_MAX_ORD = ord('\uDCFF')

#endregion


#region Numbers

def human_bytes(value: int, *, unit: str = 'iB', divider: int = 1024, decimals: int = 1, max_multiple: str|None = None) -> str:
    """
    Get a human-readable representation of a number of bytes.
    
    :param max_multiple: may be `K`, `M`, `G` or `T`.
    """
    return human_number(value, unit=unit, divider=divider, decimals=decimals, max_multiple=max_multiple)


def human_number(value: int, *, unit: str = '', divider: int = 1000, decimals: int = 1, max_multiple: str|None = None) -> str:
    """
    Get a human-readable representation of a number.

    :param max_multiple: may be `K`, `M`, `G` or `T`.
    """
    if value is None:
        return None

    suffixes = []

    # Append non-multiple suffix (bytes)
    # (if unit is 'iB' we dont display the 'i' as it makes more sens to display "123 B" than "123 iB")
    if unit:
        suffixes.append(' ' + (unit[1:] if len(unit) >= 2 and unit[0] == 'i' else unit))
    else:
        suffixes.append('')

    # Append multiple suffixes
    for multiple in ['K', 'M', 'G', 'T']:
        suffixes.append(f' {multiple}{unit}')
        if max_multiple and max_multiple.upper() == multiple:
            break

    i = 0
    suffix = suffixes[i]
    divided_value = value

    while divided_value > 1000 and i < len(suffixes) - 1:
        divided_value /= divider
        i += 1
        suffix = suffixes[i]

    # Format value
    formatted_value = ('{0:,.'+('0' if i == 0 else str(decimals))+'f}').format(divided_value)
    
    # Display formatted value with suffix
    return f'{formatted_value}{suffix}'

#endregion


#region Files
#(shortcut compatible with sudo)

def read_bytes(path: str|os.PathLike, *, sudo = False) -> bytes:
    """
    Open the file in bytes mode, read it, and close the file.
    """
    if not sudo or os.access(path, os.R_OK):
        with open(path, mode='rb') as fp:
            return fp.read()
    
    from zut.process import SudoNotAvailable, is_sudo_available, run_process
    if not is_sudo_available():
        raise SudoNotAvailable()
    
    tmp = mktemp()
    try:
        run_process(['cp', path, tmp], check=True, sudo=True)
        run_process(['chown', getuser(), tmp], check=True, sudo=True)
        with open(tmp, 'rb') as fp:
            return fp.read()
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def read_text(path: str|os.PathLike, *, encoding: str|None = None, errors: str|None = None, newline: str|None = None, sudo = False) -> str:
    """
    Open the file in text mode, read it, and close the file.
    """
    if not sudo or os.access(path, os.R_OK):
        with open(path, mode='r', encoding=encoding, errors=errors, newline=newline) as fp:        
            skip_utf8_bom(fp, encoding)
            return fp.read()
    
    from zut.process import SudoNotAvailable, is_sudo_available, run_process
    if not is_sudo_available():
        raise SudoNotAvailable()
    
    tmp = mktemp()
    try:
        run_process(['cp', path, tmp], check=True, sudo=True)
        run_process(['chown', getuser(), tmp], check=True, sudo=True)
        with open(tmp, 'r', encoding=encoding, errors=errors, newline=newline) as fp:
            return fp.read()
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def write_bytes(path: str|os.PathLike, data, *, sudo = False):
    """
    Open the file in bytes mode, write to it, and close the file.
    """
    if not sudo or os.access(path, os.W_OK):
        with open(path, mode='wb') as fp:
            fp.write(data)
        return
    
    from zut.process import SudoNotAvailable, is_sudo_available, run_process
    if not is_sudo_available():
        raise SudoNotAvailable()

    tmp = mktemp()
    try:
        with open(tmp, mode='wb') as fp:
            fp.write(data)
        run_process(['cp', tmp, path], check=True, sudo=True)
    finally:
        os.unlink(tmp)


def write_text(path: str|os.PathLike, data: str, *, encoding: str|None = None, errors: str|None = None, newline: str|None = None, sudo = False):
    """
    Open the file in text mode, write to it, and close the file.
    """
    if not sudo or os.access(path, os.W_OK):
        with open(path, mode='w', encoding=encoding, errors=errors, newline=newline) as fp:
            fp.write(data)
        return
    
    from zut.process import SudoNotAvailable, is_sudo_available, run_process
    if not is_sudo_available():
        raise SudoNotAvailable()

    tmp = mktemp()
    try:
        with open(tmp, mode='w', encoding=encoding, errors=errors, newline=newline) as fp:
            fp.write(data)
        run_process(['cp', tmp, path], check=True, sudo=True)
    finally:
        os.unlink(tmp)

#endregion


#region Colors

class Color:
    RESET = '\033[0m'

    BLACK = '\033[0;30m'
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[0;33m'
    BLUE = '\033[0;34m'
    PURPLE = '\033[0;35m'
    CYAN = '\033[0;36m'
    WHITE = '\033[0;37m'
    GRAY = LIGHT_BLACK = '\033[0;90m'
    BG_RED = '\033[0;41m'

    # Disable coloring if environment variable NO_COLORS is set to 1 or if stderr is piped/redirected
    NO_COLORS = False
    if os.environ.get('NO_COLORS', '').lower() in {'1', 'yes', 'true', 'on'} or not sys.stderr.isatty():
        NO_COLORS = True
        for _ in dir():
            if isinstance(_, str) and _[0] != '_' and _ not in ['DISABLED']:
                locals()[_] = ''

    # Set Windows console in VT mode
    if not NO_COLORS and sys.platform == 'win32':
        import ctypes
        _kernel32 = ctypes.windll.kernel32
        _kernel32.SetConsoleMode(_kernel32.GetStdHandle(-11), 7)
        del _kernel32

#endregion


#region Errors

class SimpleError(ValueError):
    """
    An error that should result to only an error message being printed on the console, without a stack trace.
    """
    def __init__(self, msg: str, *args, **kwargs):
        if args or kwargs:
            msg = msg.format(*args, **kwargs)
        super().__init__(msg)

#endregion


#region Settings usage

@runtime_checkable
class DelayedStr(Protocol):
    @property
    def value(self) -> str|None:
        ...

    @classmethod
    def ensure_value(cls, obj: str|DelayedStr|None) -> str|None:
        if obj is None or isinstance(obj, str):
            return obj
        else:
            return obj.value
        

class Secret(DelayedStr):
    def __init__(self, name: str, default: type[SecretNotFound]|str|None = None):
        self.name = name
        self.default = default
        self._is_evaluated = False
        self._value = None
    
    def __str__(self):
        return f"Secret({self.name})"
    
    def __repr__(self):
        return f"Secret({self.name})"

    @property
    def is_evaluated(self):
        return self._is_evaluated
    
    @property
    def value(self) -> str|None:
        if not self._is_evaluated:
            get_logger(__name__).debug("Evaluate secret %s", self.name)
            self._value = get_secret_value(self.name, self.default)
            self._is_evaluated = True
        return self._value


class SecretNotFound(Exception):
    def __init__(self, name: str):
        self.name = name
        super().__init__(f"Secret '{name}' not found")


def get_secret_value(name: str, default: type[SecretNotFound]|str|None = None) -> str|None:
    # Search in standard files
    name = name.lower()
    if (path := Path(f'/run/secrets/{name}')).exists(): # usefull in Docker containers
        return path.read_text(encoding='utf-8')
    elif (path := Path.cwd().joinpath(f'secrets/{name}')).exists(): # usefull during local development
        return path.read_text(encoding='utf-8')
    
    # Search in environment variables
    name = name.upper()
    if value := os.environ.get(name):
        return value
    elif file := os.environ.get(f'{name}_FILE'):
        if m := re.match(r'^pass:(?P<pass_name>.+)$', file):
            from zut.gpg import get_pass
            return get_pass(m['pass_name'], default)
        
        else:
            with open(file, 'r', encoding='utf-8-sig') as fp:
                return fp.read().rstrip('\r\n')

    # Return default
    if isinstance(default, type):
        raise default(name)
    return default


def is_secret_defined(name: str):
    # Search in standard files
    name = name.lower()
    if Path(f'/run/secrets/{name}').exists(): # usefull in Docker containers
        return True
    elif Path.cwd().joinpath(f'secrets/{name}').exists(): # usefull during local development
        return True
    
    # Search in environment variables
    name = name.upper()
    if os.environ.get(name):
        return True
    elif os.environ.get(f'{name}_FILE'):
        return True
    
    # Return default
    return False

#endregion


#region Logging usage
# (see `zut.logging` for configuration of logging)

def get_logger(obj: str|type|object):
    if isinstance(obj, str):
        name = obj
    else:
        if isinstance(obj, type):
            name = f'{obj.__module__}.{obj.__qualname__}'
        elif hasattr(obj, '__class__'):
            name = f'{obj.__class__.__module__}.{obj.__class__.__qualname__}'
        else:
            raise TypeError(f"Invalid type for `get_logger` argument: {type(obj).__name__}")

    try:
        from celery.utils.log import get_task_logger  # type: ignore
        return get_task_logger(name)
    except ModuleNotFoundError:
        return logging.getLogger(name)


@contextmanager
def log_warnings(*, ignore: str|re.Pattern|list[str|re.Pattern]|None = None, logger: logging.Logger|None = None):
    catch = catch_warnings(record=True)
    ctx = None
    try:
        ctx = catch.__enter__()
        yield None
    
    finally:
        if not logger:
            logger = get_logger(__name__)
        if isinstance(ignore, (str,re.Pattern)):
            ignore = [ignore]

        if ctx is not None:
            for warning in ctx:
                ignored = False
                if ignore:
                    message = str(warning.message)
                    for spec in ignore:
                        if isinstance(spec, re.Pattern):
                            if spec.match(message):
                                ignored = True
                                break
                        elif spec == message:
                            ignored = True
                            break
                
                if not ignored:
                    logger.warning("%s: %s", warning.category.__name__, warning.message)
        
        catch.__exit__(None, None, None)

#endregion
