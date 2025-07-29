import io
import pathlib
import shutil
from typing import List, Union

from dataheroes.data import helpers
from dataheroes.data.storage.storage import Storage
import os

class StorageLocal(Storage):
    def read_bytes(self, storage_path: str, local_copy_dir: str = None) -> io.BytesIO:
        if local_copy_dir:
            local_path = pathlib.Path(
                local_copy_dir, self._get_abs_path_no_root(storage_path)
            )
            if not local_path.exists():
                local_path.parent.mkdir(parents=True, exist_ok=True)
                self.storage_to_local(storage_path, str(local_path))
            return helpers.localpath_to_bytestream(local_path)
        return helpers.localpath_to_bytestream(storage_path)

    def dump_bytes(self, data: bytes, path: str) -> str:
        with open(path, "wb") as file:
            file.write(data)
        return path

    def storage_to_local(
        self, storage_path: str, local_path: Union[str, os.PathLike]
    ) -> str:
        if not self.is_file(str(storage_path)):
            raise FileNotFoundError(
                f"Path {str(storage_path)} doesn't exist or is a directory."
            )
        local_path = pathlib.Path(str(local_path))
        if not local_path.exists():
            local_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(str(storage_path), str(local_path))
        return str(local_path)

    def local_to_storage(
        self, local_path: Union[str, os.PathLike], storage_path: str
    ) -> str:
        if not os.path.exists(local_path):
            raise FileNotFoundError(f"Path {local_path} could not be found")
        return shutil.copy(local_path, storage_path)

    def iterdir(self, dir_path: str, include_dirs: bool = False) -> List[str]:
        if not self.exists(dir_path):
            raise FileNotFoundError(f"Path {dir_path} could not be found")
        if self.is_file(dir_path):
            return [dir_path]
        files = []
        for file_name in os.listdir(dir_path):
            if not include_dirs and self.is_dir(self.joinpath(dir_path, file_name)):
                continue
            files.append(file_name)
        return [self.joinpath(dir_path, file) for file in files]

    def exists(self, path: str) -> bool:
        return os.path.exists(path)

    def is_dir(self, path: str) -> bool:
        return pathlib.Path(path).is_dir()
    
    def is_file(self, path: str) -> bool:
        return pathlib.Path(path).is_file() 

    def is_absolute(self, path: str) -> bool:
        return pathlib.Path(path).is_absolute()

    def mkdir(
        self, dir_path: str, parents: bool = False, exist_ok: bool = False
    ) -> None:
        pathlib.Path(dir_path).mkdir(parents=parents, exist_ok=exist_ok)
    
    def remove_dir(self, path: str) -> None:
        try:
            shutil.rmtree(path)
        except FileNotFoundError:
            pass

    def joinpath(self, dir_path: Union[str, os.PathLike], path: Union[str, os.PathLike]) -> str:
        dir_path = pathlib.Path(dir_path)
        return str(dir_path / path)
    
    def parents(self, path: str) -> List[str]:
        parents = list(pathlib.Path(path).parents)
        parents = [str(parent) for parent in parents]
        # This avoids having an empty list as a result
        return parents or [path]

    def parent(self, path: str) -> str:
        return self.parents(path)[0]

    def stem(self, path: str) -> str:
        return pathlib.Path(path).stem

    def name(self, path: str) -> str:
        return pathlib.Path(path).name

    def _get_abs_path_no_root(self, path: str) -> str:
        abs_path = os.path.abspath(path)
        parts = pathlib.Path(abs_path).parts
        return str(pathlib.Path(*parts[1:]))
