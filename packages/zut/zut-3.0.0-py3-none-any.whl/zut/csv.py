import csv
import json
import locale
import os
import re
import sys
from contextlib import contextmanager, nullcontext
from datetime import datetime, time, tzinfo
from decimal import Decimal
from enum import Enum, Flag
from io import StringIO
from tempfile import NamedTemporaryFile
from typing import IO, Any, Iterable, Literal, Mapping, Sequence, overload

from zut import UTF8_BOM, get_logger, skip_utf8_bom


def get_csv_columns(file: str|os.PathLike|IO[str], *, encoding = 'utf-8', delimiter: str|None = None, quotechar = '"'):
    columns, _, _ = examine_csv_file(file, encoding=encoding, delimiter=delimiter, quotechar=quotechar, need_ends_with_newline=False)
    return columns


def examine_csv_file(file: str|os.PathLike|IO[str], *, encoding = 'utf-8', delimiter: str|None = None, quotechar = '"', warn_distinct_guessed_delimiter = True, need_ends_with_newline = True) -> tuple[list[str]|None,str|None,bool|None]:
    """
    Returns `(columns, guessed_delimiter, ends_with_newline)`
    """
    columns = None
    ends_with_newline = None

    if isinstance(file, (str,os.PathLike)):
        if not os.path.exists(file):
            raise FileNotFoundError(f"CSV file not found: {file}")

    first_line_io = StringIO()
    with open(file, 'r', encoding='utf-8' if encoding == 'utf-8-sig' else encoding, newline='') if isinstance(file, (str,os.PathLike)) else nullcontext(file) as fp:
        skip_utf8_bom(fp, encoding)

        first_line_ended = False
        buf_size = 65536
        while True:
            chunk = fp.read(buf_size)
            if not chunk:
                break

            if not first_line_ended:
                pos = chunk.find('\n')
                if pos >= 0:
                    first_line_io.write(chunk[:pos])
                    first_line_ended = True
                    if not need_ends_with_newline:
                        break
                else:
                    first_line_io.write(chunk)

            if need_ends_with_newline:
                ends_with_newline = chunk[-1] == '\n'

    if first_line_io.tell() == 0:
        return columns, delimiter, ends_with_newline

    # Guess the delimiter
    first_line_str = first_line_io.getvalue()
    comma_count = first_line_str.count(',')
    semicolon_count = first_line_str.count(';')

    if semicolon_count > comma_count:
        guessed_delimiter = ';'
    elif comma_count > 0:
        guessed_delimiter = ','
    else:
        guessed_delimiter = delimiter or CsvWriter.get_default_delimiter()

    # Compare with the given delimiter
    if delimiter:
        if guessed_delimiter and guessed_delimiter != delimiter:
            if warn_distinct_guessed_delimiter:
                get_logger(__name__).warning("Guessed CSV delimiter (\"%s\") is distinct from given CSV delimiter (\"%s\") for %s", guessed_delimiter, delimiter, file)

    # Retrieve column names
    first_line_io.seek(0)
    reader = csv.reader(first_line_io, delimiter=guessed_delimiter, quotechar=quotechar, doublequote=True)
    columns = next(reader)

    # Ensure we move back the fp if it was externally built
    if not isinstance(file, (str,os.PathLike)):
        file.seek(0)
        skip_utf8_bom(file, encoding)

    return columns, guessed_delimiter, ends_with_newline


def escape_csv_value(value, *, delimiter: str|None = None, quotechar = '"', nullval: str|None = None):
    if value is None:    
        return nullval if nullval is not None else ''
    if not isinstance(value, str):
        value = str(value)
    if value == '':
        return f'{quotechar}{quotechar}'
    
    if not delimiter:
        delimiter = CsvWriter.get_default_delimiter()

    need_escape = False
    result = ''
    for c in value:
        if c == delimiter:
            result += c
            need_escape = True
        elif c == quotechar:
            result += f'{c}{c}'
            need_escape = True
        elif c == '\n' or c == '\r':
            result += c
            need_escape = True
        else:
            result += c

    if need_escape:
        result = f'{quotechar}{result}{quotechar}'
    else:
        result = result

    return result


def format_csv_value(value, *, decimal_separator = '.', no_tz: bool|tzinfo|Literal['localtime'] = False, no_microseconds = False, visual = False):    
    def format_value(value, *, root):    
        if value is None:
            return None

        if no_tz and isinstance(value, str):
            if re.match(r'^\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(?:\.\d{3,6})?(?:Z|[+\-\d]{2,5})?$', value): # recognize datetime ISO strings (typically comming from APIs with JSON-encoded data) and handle them later as datetimes
                value = datetime.fromisoformat(value)

        if isinstance(value, (Enum,Flag)):
            return value.name if visual else value.value
            
        elif isinstance(value, bool):
            if visual:
                return value # Excel and tabulate will be able to handle them as such
            else:
                return 'true' if value else 'false'
        
        elif isinstance(value, int):
            return value
        
        elif isinstance(value, (float,Decimal)):
            str_value = format(value, 'f') # avoid scientific notation
            if decimal_separator != '.':
                return str_value.replace('.', decimal_separator)        
            return str_value
        
        elif isinstance(value, (datetime,time)):
            if no_tz:
                if value.tzinfo and isinstance(value, datetime): # make the datetime naive if it is not already
                    if value.year >= 2999: # avoid astimezone() issue for conversion of datetimes such as 9999-12-31 23:59:59.999999+00:00 or 4000-01-02 23:00:00+00:00
                        value = value.replace(tzinfo=None)
                    else:
                        value = value.astimezone(None if no_tz is True or no_tz == 'localtime' else no_tz).replace(tzinfo=None)
            if no_microseconds:
                return value.replace(microsecond=0)
            return value

        elif isinstance(value, (list,tuple)):
            if visual:
                if root:
                    if len(value) == 1:
                        return format(value[0])
                    
                    from zut.convert import get_visual_iterable_literal
                    return get_visual_iterable_literal(value)
                
                from zut.json import ExtendedJSONEncoder
                return json.dumps(value, ensure_ascii=False, cls=ExtendedJSONEncoder)

            else:
                from zut.convert import get_postgresql_array_literal
                return get_postgresql_array_literal(value)
        
        elif isinstance(value, dict):
            if visual and root:
                from zut.convert import get_visual_mapping_literal
                return get_visual_mapping_literal(value)
            
            else:
                from zut.json import ExtendedJSONEncoder
                return json.dumps(value, ensure_ascii=False, cls=ExtendedJSONEncoder)
                
        else:
            return value

    return format_value(value, root=True)


@overload
def format_csv_row(row: Iterable, *, delimiter: str|None = None, decimal_separator = '.', no_tz: bool|tzinfo|Literal['localtime'] = False, no_microseconds = False, visual = False, as_string: Literal[False] = ...) -> list[Any]:
    ...

@overload
def format_csv_row(row: Iterable, *, delimiter: str|None = None, decimal_separator = '.', no_tz: bool|tzinfo|Literal['localtime'] = False, no_microseconds = False, visual = False, as_string: Literal[True]) -> str:
    ...

def format_csv_row(row: Iterable, *, delimiter: str|None = None, decimal_separator = '.', no_tz: bool|tzinfo|Literal['localtime'] = False, no_microseconds = False, visual = False, as_string = False) -> list[Any]|str:
    if as_string:
        target = ''
        if delimiter is None:
            delimiter = CsvWriter.get_default_delimiter()
    else:
        target = []

    first = True
    for value in row:
        formatted_value = format_csv_value(value, decimal_separator=decimal_separator, no_tz=no_tz, no_microseconds=no_microseconds, visual=visual)
        if as_string:
            if first:
                first = False
            else:
                target += delimiter # type: ignore (as_string => target is a string)
            target += escape_csv_value(formatted_value)
        else:
            target.append(formatted_value) # type: ignore (not as_string => target is a list)
    return target



# ROADMAP: add a delay option

class CsvWriter:
    delimiter: str|None = None
    for_excel: bool|None = None

    def __init__(self, file:str|os.PathLike|IO[str]|None = None, headers: Iterable[str]|None = None, *, tz: tzinfo|Literal['localtime']|str|None = None, encoding = 'utf-8-sig', delimiter: str|None = None, for_excel: bool|None = None):
        self._logger = get_logger(self.__class__)

        self.tz: tzinfo|Literal['localtime']|None
        if tz is None:
            self.tz = None
        elif isinstance(tz, tzinfo) or tz == 'localtime':
            self.tz = tz
        else:
            from zut.timezone import parse_timezone
            self.tz = parse_timezone(tz)
        
        self._headers: list[str]|None = None
        self.encoding = encoding
        self.delimiter = delimiter if delimiter else self.get_default_delimiter()
        self.for_excel = for_excel if for_excel is not None else self.get_default_for_excel()

        self._file: IO[str]|None
        self.name: str

        if file is None:
            temp = NamedTemporaryFile('w', encoding=self.encoding, newline='', suffix='.csv', delete=False).__enter__()
            self.name = temp.name
            self._file = temp.file # type: ignore
            self._must_close_file = temp
        elif isinstance(file, (str, os.PathLike)):
            self.name = str(file) if not isinstance(file, str) else file
            self._file = None
            self._must_close_file = True # self
        else:
            self.name = str(file)
            self._file = file # type: ignore
            self._must_close_file = False # external
        
        self._must_insert_newline = False
        self.rowcount = 0

        if headers is not None:
            self.headers = headers

    def close(self):
        if self._must_close_file and self._file:
            if self._must_close_file is True:
                self._file.close()
            else:
                self._must_close_file.close()
            self._file = None

    def __enter__(self):
        return self
    
    def __exit__(self, *exc_info):
        self.close()

    @property
    def file(self) -> IO[str]:
        if self._file is None:
            parent = os.path.dirname(self.name)
            if parent and not os.path.exists(parent):
                os.makedirs(parent)

            self._file = open(self.name, 'w', encoding=self.encoding, newline='')
        
        return self._file # type: ignore
    
    @property
    def is_headers_set(self):
        return self._headers is not None

    @property
    def headers(self):
        if self._headers is None:
            raise ValueError("Headers not set")
        return self._headers
    
    @headers.setter
    def headers(self, headers: Iterable[str]):
        if self._headers is not None:
            raise ValueError("Headers already set")
        self._headers = [str(header) for header in headers]
        self.writerow(self.headers, no_rowcount=True)

    def writerow(self, row: Sequence[Any]|Mapping[str,Any], *, no_rowcount = False):
        if not no_rowcount:
            self.rowcount += 1

        if isinstance(row, Mapping):
            row = self._get_mapping_row(row)

        decimal_separator = '.'
        no_tz = False
        no_microseconds = False
        if self.for_excel:
            if self.delimiter == ';':
                decimal_separator = ','            
            no_tz = self.tz if self.tz else True
            no_microseconds = True
        
        row = format_csv_row(row, delimiter=self.delimiter, decimal_separator=decimal_separator, no_tz=no_tz, no_microseconds=no_microseconds, as_string=True)
        if self._must_insert_newline:
            self.file.write('\n')
        else:
            self._must_insert_newline = True
        self.file.write(row)
        self.file.flush()

    def _get_mapping_row(self, row: Mapping[str,Any]):
        if not self.is_headers_set:
            self.headers = [str(key) for key in row]
        
        actual_row = []
        missing_keys = []
        for header in self.headers:
            if header in row:
                value = row[header]
            else:
                value = None
                missing_keys.append(header)
            actual_row.append(value)

        if missing_keys:
            self._logger.warning(f"Missing header key(s) for row {self.rowcount}: {', '.join(missing_keys)}")

        ignore_keys = []
        for key in row:
            if not key in self.headers:
                ignore_keys.append(key)

        if ignore_keys:
            self._logger.warning(f"Ignore additional key(s) missing for row {self.rowcount}: {', '.join(ignore_keys)}")

        return actual_row

    @classmethod
    def get_default_delimiter(cls):
        if not cls.delimiter:
            cls.delimiter = os.environ.get('CSV_DELIMITER')
            if not cls.delimiter:
                from zut.config import use_locale
                with use_locale():
                    decimal_point = locale.localeconv()["decimal_point"]
                cls.delimiter = ';' if decimal_point == ',' else ','
        
        return cls.delimiter

    @classmethod
    def get_default_for_excel(cls):
        if cls.for_excel is None:
            cls.for_excel = os.environ.get('CSV_FOR_EXCEL', '0').lower() in {'1', 'true', 'yes', 'on'}
        
        return cls.for_excel


class CsvReader:
    def __init__(self, file: str|os.PathLike|IO[str], headers: Iterable[str]|None = None, *, encoding = 'utf-8', delimiter: str|None = None, no_headers = False):
        self._logger = get_logger(self.__class__)

        self._file: IO[str]|None
        self.name: str

        if isinstance(file, (str, os.PathLike)):
            self.name = str(file) if not isinstance(file, str) else file
            self._file = None
            self._must_close_file = True # self
        else:
            self.name = str(file)
            self._file = file # type: ignore
            self._must_close_file = False # external
        
        self._actual_reader = None

        self._headers = [header for header in headers] if headers is not None else None
        self.encoding = encoding
        self.delimiter = delimiter
        self.no_headers = no_headers
        self._file_headers: list[str]|None = None
        self._headers_reindex: Sequence[int|None]|None = None
        
        self.rowcount = 0

    def close(self):
        if self._must_close_file and self._file:
            self._file.close()
            self._file = None

    def __enter__(self):
        return self
    
    def __exit__(self, *exc_info):
        self.close()

    @property
    def file(self) -> IO[str]:
        if self._file is None:
            self._file = open(self.name, 'r', encoding=self.encoding, newline='')
        
        return self._file # type: ignore

    @property
    def actual_reader(self):
        if self._actual_reader is None:
            if self.delimiter is None:
                columns, delimiter, _ = examine_csv_file(self.file, encoding=self.encoding)
                self.delimiter = delimiter or CsvWriter.get_default_delimiter()
            else:
                skip_utf8_bom(self.file, self.encoding)

            if sys.version_info >= (3, 13): # NOTE: QUOTE_NOTNULL does not seem to work correctly on Python 3.12
                self._actual_reader = csv.reader(self.file, delimiter=self.delimiter, quoting=csv.QUOTE_NOTNULL)
                self._auto_unquote_null = True
            else:
                self._actual_reader = csv.reader(self.file, delimiter=self.delimiter)
                self._auto_unquote_null = False
                
        return self._actual_reader
    
    def _ensure_headers_read(self):
        if self._file_headers is not None:
            return # already read
        
        if self.no_headers:
            if not self._headers:
                raise ValueError("CsvReader argument `headers` is required when the file has no headers")
            return
        
        self._file_headers = next(self.actual_reader)
        if len(self._file_headers) >= 1 and len(self._file_headers[0]) >= 1 and self._file_headers[0][0] == UTF8_BOM:
            self._file_headers[0] = self._file_headers[0][1:]
        
        if self._headers is None:
            self._headers = self._file_headers
        elif self._headers == self._file_headers:
            pass # No reindex to do
        else:
            indexes = {header: index for index, header in enumerate(self._file_headers)}
            self._headers_reindex = []
            missing_headers = []
            for header in self._headers:
                index = indexes.get(header)
                if index is None:
                    missing_headers.append(header)
                self._headers_reindex.append(index)

            if missing_headers:
                self._logger.warning(f"Missing header(s) in CSV file {self.name}: {', '.join(missing_headers)}")
    
    @property
    def file_headers(self) -> list[str]:        
        self._ensure_headers_read()
        return self._file_headers # type: ignore (cannot be None)
    
    @property
    def headers(self) -> list[str]:
        self._ensure_headers_read()
        return self._headers # type: ignore (cannot be None)
    
    def __iter__(self):
        return self

    def __next__(self):
        self._ensure_headers_read()
        actual_row = next(self.actual_reader)
        self.rowcount += 1
        
        row: list[str|None]
        if self._headers_reindex is not None:
            row = [actual_row[index] if index is not None and index < len(actual_row) else None for index in self._headers_reindex]
        else:
            row = actual_row # type: ignore

        if not self._auto_unquote_null:
            for i in range(len(row)):
                if row[i] == '':
                    row[i] = None

        return row
    
    def next_dict(self):
        return self._convert_to_dict(next(self))
    
    def iter_dicts(self):
        for row in self:
            yield self._convert_to_dict(row)

    def _convert_to_dict(self, row: Sequence[str|None]):        
        if len(row) < len(self.headers):
            missing_columns = self.headers[len(row):]
            self._logger.warning(f"Missing column(s) for row {self.rowcount}: {', '.join(missing_columns)}")
        elif len(row) > len(self.headers):
            ignore_columns = f"{len(row)+1}-{len(self.headers)}"
            self._logger.warning(f"Ignore additional column(s) for row {self.rowcount}: {ignore_columns}")

        return {header: row[i] if i < len(row) else None for i, header in enumerate(self.headers)}
    

def dump_csv(data: Any, file: str|os.PathLike|IO[str], headers: Iterable[str]|None = None, *, tz: tzinfo|Literal['localtime']|str|None = None, encoding = 'utf-8-sig', delimiter: str|None = None, for_excel: bool|None = None):
    with CsvWriter(file, headers, tz=tz, encoding=encoding, delimiter=delimiter, for_excel=for_excel) as writer:
        for row in data:
            writer.writerow(row)


@contextmanager
def dump_csv_temp(data: Any, headers: Iterable[str]|None = None, *, tz: tzinfo|Literal['localtime']|str|None = None, encoding = 'utf-8-sig', delimiter: str|None = None, for_excel: bool|None = None):
    temp = None
    try:
        with NamedTemporaryFile('w', encoding=encoding, newline='', suffix='.csv', delete=False) as temp:
            dump_csv(data, temp.file, headers=headers, tz=tz, encoding=encoding, delimiter=delimiter, for_excel=for_excel)
 
        yield temp.name
    finally:
        if temp is not None:
            os.unlink(temp.name)


def load_csv(file: str|os.PathLike|IO[str], headers: Iterable[str]|None = None, *, encoding = 'utf-8', delimiter: str|None = None, no_headers = False) -> list[dict[str,Any]]:
    with CsvReader(file, headers, encoding=encoding, delimiter=delimiter, no_headers=no_headers) as reader:
        return [data for data in reader.iter_dicts()]
