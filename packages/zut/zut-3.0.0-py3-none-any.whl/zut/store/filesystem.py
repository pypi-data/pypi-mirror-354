from typing import IO, Any, ContextManager

from django.core.files.storage.filesystem import FileSystemStorage

from . import ExtendedStorage


class FileSystemExtendedStorage(ExtendedStorage, FileSystemStorage):
    @classmethod
    def get_storage_kwargs_from_path(cls, location: Any) -> dict[str,Any]:
        return {'location': location}
  
    @property
    def is_versioning_enabled(self) -> bool:
        return False

    def open(self, name: str, mode: str = 'rb', *, encoding: str|None = None, newline: str|None = None) -> ContextManager[IO]:
        return open(self.path(name), mode, encoding=encoding, newline=newline)
