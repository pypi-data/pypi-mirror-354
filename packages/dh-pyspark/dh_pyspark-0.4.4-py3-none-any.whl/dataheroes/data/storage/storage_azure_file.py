import io
import os
import pathlib
from typing import List, Tuple, Union
from urllib.parse import urlparse
from dataheroes.configuration import DataHeroesConfiguration
from dataheroes.data import helpers
from dataheroes.data.storage.storage import Storage
from azure.storage.fileshare import (
    ShareServiceClient,
    ShareFileClient,
    ShareDirectoryClient,
)


class StorageAzureFile(Storage):
    def __init__(self) -> None:
        config = DataHeroesConfiguration()
        connection_string = config.get_param(
            name="storage_connection_string", section="azure"
        )
        try:
            self._process_connection_string(connection_string)
            self.client = ShareServiceClient.from_connection_string(connection_string)
        except Exception as e:
            msg = (
                "Exception while creating Azure File Storage client. Check DataHeroes config file"
                + "or use the dataheroes.cli script to configure credentials for Azure File Storage.\n"
            )
            msg += str(e)
            raise Exception(msg) from e

    def read_bytes(self, storage_path: str, local_copy_dir: str = None) -> io.BytesIO:
        if local_copy_dir:
            _, file_name = self._parse_url(storage_path)
            local_path = pathlib.Path(local_copy_dir, file_name)
            if not local_path.exists():
                local_path.parent.mkdir(parents=True, exist_ok=True)
                self.storage_to_local(storage_path, str(local_path))
            return helpers.localpath_to_bytestream(local_path)
        file = self._get_file(storage_path)
        data = file.download_file().readall()
        return helpers.bytes_to_bytestream(data)

    def dump_bytes(self, data: bytes, path: str) -> None:
        file = self._get_file(path)
        file.upload_file(data)

    def storage_to_local(
        self, storage_path: str, local_path: Union[str, os.PathLike]
    ) -> str:
        if not self.is_file(storage_path):
            raise FileNotFoundError(
                f"Path {storage_path} doesn't exist or is a directory."
            )
        local_path = pathlib.Path(local_path)
        if not local_path.exists():
            local_path.parent.mkdir(parents=True, exist_ok=True)
            with open(local_path, "wb") as f:
                f.write(self.read_bytes(storage_path).getvalue())
        return str(local_path)

    def local_to_storage(
        self, local_path: Union[str, os.PathLike], storage_path: str
    ) -> str:
        file = self._get_file(storage_path)
        with open(local_path, "rb") as f:
            file.upload_file(f)
        return storage_path

    def iterdir(self, dir_path: str, include_dirs: bool = False) -> List[str]:
        if not self.exists(dir_path):
            raise FileNotFoundError(f"Path {dir_path} could not be found")
        if self.is_file(dir_path):
            return [dir_path]
        share_name, dir_name = self._parse_url(dir_path)
        dir = self._get_dir(dir_path)
        result = []
        if not dir.exists():
            file = self._get_file(dir_name)
            if file.exists():
                result = ["/".join(file.file_path)]
            else:
                result = []
        else:
            sub_dir = list(dir.list_directories_and_files())
            for item in sub_dir:
                if item["is_directory"] == True:
                    if not include_dirs:
                        continue
                    item_path = dir.get_subdirectory_client(item["name"]).directory_path
                else:
                    item_path = "/".join(dir.get_file_client(item["name"]).file_path)
                result.append(item_path)

        result = [
            self._filename_to_azureuri(share_name, sub_path) for sub_path in result
        ]
        return list(set(result))

    def exists(self, path: str) -> bool:
        return self.is_file(path) or self.is_dir(path)

    def is_dir(self, path: str) -> bool:
        dir = self._get_dir(path)
        return dir.exists()

    def is_file(self, path: str) -> bool:
        if path[-1] == "/":
            return False
        file = self._get_file(path)
        return file.exists()

    def is_absolute(self, path: str) -> bool:
        return path.startswith(self.endpoint_protocol)

    def mkdir(
        self, dir_path: str, parents: bool = False, exist_ok: bool = False
    ) -> None:
        if self.exists(dir_path) and not exist_ok:
            raise FileExistsError(f"Path {dir_path} already exists")
        parent = self.parent(dir_path)
        if not self.exists(parent) and not parents:
            raise FileNotFoundError(f"Path {parent} doesn't exist")
        for path in self.parents(dir_path)[::-1]:
            if not self.exists(path):
                path = self._get_dir(path)
                path.create_directory()
        dir = self._get_dir(dir_path)
        if not dir.exists():
            dir.create_directory()

    def remove_dir(self, dir_path: str) -> None:
        if not self.is_dir(dir_path):
            raise ValueError(f"Path is not a dir: {dir_path}")
        dir = self._get_dir(dir_path)
        sub_files = dir.list_directories_and_files()
        for file in sub_files:
            if file["is_directory"]:
                self._remove_dir_client(dir.get_subdirectory_client(file["name"]))
            else:
                dir.get_file_client(file["name"]).delete_file()
        dir.delete_directory()

    def _remove_dir_client(self, dir_client: ShareDirectoryClient) -> None:
        sub_files = dir_client.list_directories_and_files()
        for file in sub_files:
            if file["is_directory"]:
                self._remove_dir_client(
                    dir_client.get_subdirectory_client(file["name"])
                )
            else:
                dir_client.get_file_client(file["name"]).delete_file()
        dir_client.delete_directory()

    def joinpath(self, dir_path: str, path: str) -> str:
        return dir_path.rstrip("/") + "/" + path.lstrip("/")

    def parents(self, path: str) -> List[str]:
        share_name, file_name = self._parse_url(path)
        file_name = file_name.rstrip("/")
        file_bits = file_name.split("/")
        urls = []
        if len(file_bits) == 1:
            urls.append(self._filename_to_azureuri(share_name, ""))
        else:
            for index in range(len(file_bits) - 1, -1, -1):
                parent = str.join("/", file_bits[:index])
                urls.append(self._filename_to_azureuri(share_name, parent))
        # this adds the / that indicates a directory and avoid // for the root bucket path
        urls = [url.rstrip("/") + "/" for url in urls]
        return urls

    def parent(self, path: str) -> str:
        return self.parents(path)[0]

    def stem(self, path: str) -> str:
        return self.name(path).rsplit(".", maxsplit=1)[0]

    def name(self, path: str) -> str:
        return path.rstrip("/").split("/")[-1]

    def _parse_url(self, path: str) -> Tuple[str, str]:
        parsed_url = urlparse(path)
        path_parts = parsed_url.path.lstrip("/").split("/", maxsplit=1)
        share_name = path_parts[0]
        file_name = path_parts[1]
        return share_name, file_name

    def _filename_to_azureuri(self, share_name: str, file_name: str) -> str:
        return f"{self.endpoint_protocol}://{self.account_name}.file.{self.endpoint_suffix}/{share_name}/{file_name}"

    def _get_file(self, path: str) -> ShareFileClient:
        share_name, file_name = self._parse_url(path)
        return self.client.get_share_client(share_name).get_file_client(file_name)

    def _get_dir(self, path: str) -> ShareDirectoryClient:
        share_name, dir_name = self._parse_url(path)
        return self.client.get_share_client(share_name).get_directory_client(dir_name)

    def _process_connection_string(self, connection_string) -> None:
        fields = connection_string.split(";")
        fields = [field.split("=") for field in fields]
        fields = {field[0]: field[1] for field in fields}
        self.endpoint_protocol = fields.get("DefaultEndpointProtocol", "https")
        self.endpoint_suffix = fields.get("EndpointSuffix", "core.windows.net")
        self.account_name = fields.get("AccountName", None)
        if not self.account_name:
            msg = (
                "Storage connection string doesn't contain account name. "
                + "Please check the storage connection string in dataheroes config "
                + "or use dataheroes.cli to reconfigure the storage connection string."
            )
            raise ValueError(msg)
