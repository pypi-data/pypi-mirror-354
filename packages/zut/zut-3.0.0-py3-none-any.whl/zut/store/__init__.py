import json
import logging
import os
import sys
from contextlib import contextmanager, nullcontext
from datetime import tzinfo
from functools import cached_property
from io import IOBase
from tempfile import NamedTemporaryFile
from typing import (IO, Any, ContextManager, Iterable, Literal, NamedTuple,
                    overload)

from django.core.files.storage.base import Storage

from zut import DelayedStr
from zut.csv import CsvReader, CsvWriter
from zut.json import dump_json_temp, load_json

_logger = logging.getLogger(__name__)


class ExtendedStorage(Storage):
    @classmethod
    def get_storage_kwargs_from_path(cls, location: Any) -> dict[str,Any]:
        ...
  
    @property
    def is_versioning_enabled(self) -> bool:
        """ Indicate whether the storage is able to keep several versions of the same name (without changing it to an alternate available name like FileSystemStorage does). """
        ...


    def open(self, name: str, mode: str = 'rb', *, encoding: str|None = None, newline: str|None = None) -> ContextManager[IO]:
        need_extended = False

        if encoding is not None:
            if encoding == 'utf-8':
                if sys.platform != 'linux':
                    need_extended = True
            else:
                need_extended = True
        
        if newline is not None:
            need_extended = True
        
        if need_extended:
            if mode in {'w', 'wb'}:
                return self._open_temp_write(name, mode, encoding=encoding, newline=newline)
            else:
                return self._open_temp_read(name, mode, encoding=encoding, newline=newline)
        else:
            return super().open(name, mode)


    @contextmanager
    def _open_temp_read(self, name: str, mode: str, *, encoding: str|None = None, newline: str|None = None):
        temp = None
        try:
            with self.open(name, 'rb') as fp:
                with NamedTemporaryFile(mode='wb', prefix='read-', delete=False) as temp:
                    for chunk in fp:
                        temp.file.write(chunk)

            yield open(temp.name, mode, encoding=encoding, newline=newline)
        
        finally:
            if temp:
                os.unlink(temp.name)
                

    @contextmanager
    def _open_temp_write(self, name: str, mode: str, *, encoding: str|None = None, newline: str|None = None):
        temp = None
        try:            
            with NamedTemporaryFile(mode=mode, prefix='write-', encoding=encoding, newline=newline, delete=False) as temp:
                yield temp.file
                
            with (open(temp.name, 'rb') as src, self.open(name, 'wb') as dst):
                for chunk in src:
                    dst.write(chunk)
        
        finally:
            if temp:
                os.unlink(temp.name)


class ListdirResult(NamedTuple):
    dirs: list[str]
    files: list[str]


class Store:
    def __init__(self, location: Any = None):
        self.location = location


    @cached_property
    def backend(self) -> ExtendedStorage:
        if not self.location:            
            from django.conf import settings
            self.location = getattr(settings, 'STORE_LOCATION', None)
            if not self.location:
                raise ValueError("No value found for setting STORE_LOCATION")

        backend_class = self._get_backend_class()

        kwargs = {}
        for key, value in backend_class.get_storage_kwargs_from_path(self.location).items():
            if isinstance(value, DelayedStr):
                value = value.value
            kwargs[key] = value

        return backend_class(**kwargs)
    

    def _get_backend_class(self) -> type[ExtendedStorage]:
        # May be overriden
        if isinstance(self.location, str) and self.location.startswith('s3:'):
            from .s3 import S3ExtendedStorage
            return S3ExtendedStorage
        else:
            from .filesystem import FileSystemExtendedStorage
            return FileSystemExtendedStorage


    @property
    def is_versioning_enabled(self):
        """ Indicate whether the storage is able to keep several versions of the same name (without changing it to an alternate available name like FileSystemStorage does). """
        return self.backend.is_versioning_enabled
    

    def exists(self, name: str):
        return self.backend.exists(name)
    

    @overload
    def open(self, name: str, mode: Literal['r', 'w'], *, encoding: str|None = None, newline: str|None = None) -> ContextManager[IO[str]]:
        ...

    @overload
    def open(self, name: str, mode: Literal['rb', 'wb'], *, encoding: str|None = None, newline: str|None = None) -> ContextManager[IO[bytes]]:
        ...

    def open(self, name: str, mode: Literal['r', 'w', 'rb', 'wb'], *, encoding: str|None = None, newline: str|None = None) -> ContextManager[IO]:
        return self.backend.open(name, mode, encoding=encoding, newline=newline)
    

    def listdir(self, prefix: str) -> ListdirResult:
        """
        List directories and files directly under the given prefix.

        Return empty lists if the prefix does not exist or is not a directory (contrary to FileSystemStorage's listdir which raises exceptions - not consistent with S3Storage's listdir).
        """
        try:
            dirs, files = self.backend.listdir(prefix)
            return ListdirResult(dirs, files)
        except FileNotFoundError:
            return ListdirResult([], [])
        except NotADirectoryError:
            return ListdirResult([], [])
    

    def upload(self, file: str|os.PathLike|IOBase, name: str, *, overwrite: bool|None = None) -> str:
        if overwrite is not None:
            if overwrite:
                if self.backend.exists(name):
                    _logger.debug("Delete existing %s", name)
                    self.backend.delete(name)
            else:        
                if self.backend.exists(name):
                    raise FileExistsError(f"File {name} already exists")

        with nullcontext(file) if isinstance(file, IOBase) else open(file, 'rb') as fp:
            actual_name = self.backend.save(name, fp)
            _logger.debug("Uploaded %s as %s", file, actual_name)
            return actual_name


    @contextmanager
    def open_csv_writer(self, name: str, headers: Iterable[str]|None = None, *, tz: tzinfo|Literal['localtime']|str|None = None, encoding = 'utf-8-sig', delimiter: str|None = None, for_excel: bool|None = None, overwrite: bool|None = None):
        writer = None
        try:
            writer = CsvWriter(headers=headers, tz=tz, encoding=encoding, delimiter=delimiter, for_excel=for_excel)            
            _logger.debug("Open CSV writer on temporary file %s", writer.name)
            yield writer

            writer.close() # must close now to free the temporary file
            return self.upload(writer.name, name, overwrite=overwrite)

        finally:
            if writer:
                writer.close() # in case of issue in the try clause before writer.close()
                os.unlink(writer.name)


    @contextmanager
    def open_csv_reader(self, name: str, headers: Iterable[str]|None = None, *, encoding = 'utf-8', delimiter: str|None = None, no_headers = False):
        reader = None
        file = None
        try:
            with self.open(name, 'r', encoding=encoding, newline='') as file:
                reader = CsvReader(file, headers=headers, delimiter=delimiter, no_headers=no_headers)            
                yield reader

        finally:
            if reader:
                reader.close()
            if file:
                file.__exit__(None, None, None)


    def dump_json(self, data: Any, name: str, *, encoding = 'utf-8', indent: int|None = None, sort_keys = False, ensure_ascii = False, cls: type[json.encoder.JSONEncoder]|None = None, overwrite: bool|None = None):
        with dump_json_temp(data, encoding=encoding, indent=indent, sort_keys=sort_keys, ensure_ascii=ensure_ascii, cls=cls) as tmp_name:
            self.upload(tmp_name, name, overwrite=overwrite)


    def load_json(self, name: str, *, encoding = 'utf-8', cls: type[json.decoder.JSONDecoder]|None = None):
        with self.open(name, 'r', encoding='utf-8') as fp:
            return load_json(fp, encoding=encoding, cls=cls)
