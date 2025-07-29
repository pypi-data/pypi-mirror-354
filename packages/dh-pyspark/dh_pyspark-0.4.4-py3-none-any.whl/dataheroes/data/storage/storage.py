from abc import ABC, abstractmethod
import io
import os
from typing import List, Union


class Storage(ABC):
    @abstractmethod
    def read_bytes(self, path: str, local_copy_dir: str = None) -> io.BytesIO:
        raise NotImplementedError

    @abstractmethod
    def dump_bytes(self, data: bytes, path: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def storage_to_local(self, storage_path: str, local_path: Union[str, os.PathLike]) -> str:
        raise NotImplementedError

    @abstractmethod
    def local_to_storage(self, local_path: Union[str, os.PathLike], storage_path: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def iterdir(self, path: str, include_dirs: bool = False) -> List[str]:
        raise NotImplementedError

    @abstractmethod
    def exists(self, path: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def is_dir(self, path: str) -> bool:
        raise NotImplementedError
    
    @abstractmethod
    def is_file(self, path: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def is_absolute(self, path: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def mkdir(
        self, dir_path: str, parents: bool = False, exist_ok: bool = False
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def remove_dir(self, dir_path: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def joinpath(self, dir_path: str, path: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def parents(self, path: str) -> List[str]:
        raise NotImplementedError
    
    @abstractmethod
    def parent(self, path: str) -> str:
        raise NotImplementedError
    
    @abstractmethod
    def stem(self, path: str) -> str:
        raise NotImplementedError
    
    @abstractmethod
    def name(self, path: str) -> str:
        raise NotImplementedError
    
