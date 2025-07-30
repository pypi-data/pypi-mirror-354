import io
import os
import pathlib
from typing import Any, Dict, List, Optional, Union

from dataheroes.data.storage.storage import Storage

def pathlike_to_str_args(func):
    def wrapper(*args, **kwargs):
        clean_args = []
        for arg in args:
            if isinstance(arg, os.PathLike):
                arg = str(arg)
            clean_args.append(arg)
        args = tuple(clean_args)
        for kw, arg in kwargs.items():
            if isinstance(arg, os.PathLike):
                kwargs[kw] = str(arg)
        return func(*args, **kwargs)

    return wrapper

class StorageManager(Storage):
    # StorageManager is a singleton. Only one instance can exist.
    # If an instance was created, all StorageManager() calls will return the same instance
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self):
        self.storages: Dict[str, Optional[Storage]] = {
            "aws": None,
            "gcp": None,
            "azure_blob": None,
            "azure_file": None,
            "local": None,
        }

    @pathlike_to_str_args
    def read_bytes(self, path: str, local_copy_dir: str = None) -> io.BytesIO:
        local_copy_dir = str(local_copy_dir) if local_copy_dir else None
        return self._get_storage(path).read_bytes(path, local_copy_dir)

    @pathlike_to_str_args
    def dump_bytes(self, data: bytes, path: str) -> None:
        self._get_storage(path).dump_bytes(data, path)

    @pathlike_to_str_args
    def storage_to_local(self, storage_path: str, local_path: Union[str, os.PathLike]) -> str:
        return self._get_storage(storage_path).storage_to_local(
            storage_path, local_path
        )

    @pathlike_to_str_args
    def local_to_storage(self, local_path: Union[str, os.PathLike], storage_path: str) -> str:
        return self._get_storage(storage_path).local_to_storage(
            local_path, storage_path
        )

    @pathlike_to_str_args
    def iterdir(self, path: str, *, include_dirs: bool = False) -> List[str]:
        return self._get_storage(path).iterdir(path, include_dirs=include_dirs)

    @pathlike_to_str_args
    def exists(self, path: str) -> bool:
        return self._get_storage(path).exists(path)

    @pathlike_to_str_args
    def is_dir(self, path: str) -> bool:
        return self._get_storage(path).is_dir(path)

    @pathlike_to_str_args
    def is_file(self, path: str) -> bool:
        return self._get_storage(path).is_file(path)
    
    @pathlike_to_str_args
    def is_absolute(self, path: str) -> bool:
        return self._get_storage(path).is_absolute(path)

    @pathlike_to_str_args
    def mkdir(
        self, dir_path: str, parents: bool = False, exist_ok: bool = False
    ) -> None:
        self._get_storage(dir_path).mkdir(dir_path, parents, exist_ok)
    
    @pathlike_to_str_args
    def remove_dir(self, dir_path: str) -> None:
        self._get_storage(dir_path).remove_dir(dir_path)
    
    @pathlike_to_str_args
    def joinpath(self, dir_path: str, path: str) -> str:
        return self._get_storage(dir_path).joinpath(dir_path, path)
    
    @pathlike_to_str_args
    def parents(self, path: str) -> List[str]:
        return self._get_storage(path).parents(path)
    
    @pathlike_to_str_args
    def parent(self, path: str) -> str:
        return self._get_storage(path).parent(path)

    @pathlike_to_str_args
    def stem(self, path: str) -> str:
        return self._get_storage(path).stem(path)

    @pathlike_to_str_args
    def name(self, path: str) -> str:
        return self._get_storage(path).name(path)

    @pathlike_to_str_args
    def _get_storage(self, path: str) -> Storage:
        path = path
        storage_name = self._identify_storage(path)
        if self.storages[storage_name] is None:
            print(f"Detected storage: {storage_name}. Initializing storage...")
            self.storages[storage_name] = self._create_storage(storage_name)
            print(f"Storage {storage_name} initialized.")
        return self.storages[storage_name]

    @pathlike_to_str_args
    def _identify_storage(self, path: str) -> str:
        storage_name = None
        if self.is_aws(path):
            storage_name = "aws"
        elif self.is_gcp(path):
            storage_name = "gcp"
        elif self.is_azure_blob(path):
            storage_name = "azure_blob"
        elif self.is_azure_file(path):
            storage_name = "azure_file"
        elif self.is_local(path):
            storage_name = "local"
        else:
            raise ValueError(
                f"Given path can't be associated with any of the supported cload storage solutions or local storage: {path}"
            )
        return storage_name
    
    @pathlike_to_str_args
    def _create_storage(self, storage_name: str) -> Storage:
        if storage_name == "aws":
            from dataheroes.data.storage.storage_aws import StorageAWS
            return StorageAWS()
        elif storage_name == "gcp":
            from dataheroes.data.storage.storage_gcp import StorageGCP
            return StorageGCP()
        elif storage_name == "azure_blob":
            from dataheroes.data.storage.storage_azure_blob import StorageAzureBlob
            return StorageAzureBlob()
        elif storage_name == "azure_file":
            from dataheroes.data.storage.storage_azure_file import StorageAzureFile
            return StorageAzureFile()
        elif storage_name == "local":
            from dataheroes.data.storage.storage_local import StorageLocal
            return StorageLocal()
        else:
            raise ValueError(
                f"Invalid storage name. Received {storage_name}. Expected one of: {list(self.storages.keys())}"
            )

    @pathlike_to_str_args
    def is_aws(self, path: str) -> bool:
        if path.startswith("s3://"):
            return True
        # For now this type of S3 URLs is not supported by the StorageAWS implementation
        # if path_str.startswith("http://") or path_str.startswith("https://"):
        #     if "s3" in path_str and "amazonaws.com" in path_str:
        #         return True
        return False

    @pathlike_to_str_args
    def is_gcp(self, path: str) -> bool:
        if path.startswith("gs://"):
            return True
        return False

    @pathlike_to_str_args
    def is_azure_blob(self, path: str) -> bool:
        if (
            path.startswith("http://") or path.startswith("https://")
        ) and ".blob." in path:
            return True
        return False

    @pathlike_to_str_args
    def is_azure_file(self, path: str) -> bool:
        if (
            path.startswith("http://") or path.startswith("https://")
        ) and ".file." in path:
            return True
        return False

    @pathlike_to_str_args
    def is_local(self, path: str) -> bool:
        if (
            not path.startswith("http://")
            and not path.startswith("https://")
            and not self.is_aws(path)
            and not self.is_gcp(path)
            and not self.is_azure_file(path)
            and not self.is_azure_blob(path)
        ):
            return True
        return False
