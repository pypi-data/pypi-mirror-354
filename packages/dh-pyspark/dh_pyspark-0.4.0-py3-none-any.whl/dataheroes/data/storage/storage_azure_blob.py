import io
import os
import pathlib
from typing import List, Tuple, Union
from urllib.parse import urlparse
from dataheroes.configuration import DataHeroesConfiguration
from dataheroes.data import helpers
from dataheroes.data.storage.storage import Storage
from azure.storage.blob import BlobServiceClient, BlobClient


class StorageAzureBlob(Storage):
    def __init__(self) -> None:
        config = DataHeroesConfiguration()
        connection_string = config.get_param(
            name="storage_connection_string", section="azure"
        )
        try:
            self._process_connection_string(connection_string)
            self.client = BlobServiceClient.from_connection_string(connection_string)
        except Exception as e:
            msg = (
                "Exception while creating Azure Blob Storage client. Check DataHeroes config file"
                + "or use the dataheroes.cli script to configure credentials for Azure Blob Storage.\n"
            )
            msg += str(e)
            raise Exception(msg) from e

    def read_bytes(self, storage_path: str, local_copy_dir: str = None) -> io.BytesIO:
        if local_copy_dir:
            _, blob_name = self._parse_url(storage_path)
            local_path = pathlib.Path(local_copy_dir, blob_name)
            if not local_path.exists():
                local_path.parent.mkdir(parents=True, exist_ok=True)
                self.storage_to_local(storage_path, str(local_path))
            return helpers.localpath_to_bytestream(local_path)
        blob = self._get_blob(storage_path)
        data = blob.download_blob().readall()
        return helpers.bytes_to_bytestream(data)

    def dump_bytes(self, data: bytes, path: str) -> None:
        blob = self._get_blob(path)
        blob.upload_blob(data, overwrite=True)

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
        blob = self._get_blob(storage_path)
        with open(local_path, "rb") as f:
            blob.upload_blob(f, overwrite=True)
        return storage_path

    def iterdir(self, dir_path: str, include_dirs: bool = False) -> List[str]:
        if not self.exists(dir_path):
            raise FileNotFoundError(f"Path {dir_path} could not be found")
        if self.is_file(dir_path):
            return [dir_path]
        container_name, blob_name = self._parse_url(dir_path)
        container = self.client.get_container_client(container_name)

        blobs = list(container.list_blob_names(name_starts_with=blob_name))
        result = []
        blob_name = blob_name.rstrip("/") + "/"
        for blob in blobs:
            # remove self-referential result
            if blob == blob_name:
                continue
            # remove other files or dirs with the same prefix
            if blob[len(blob_name) - 1] != "/":
                continue
            # remove subdirs if include_dirs == False
            if "/" in blob[len(blob_name) :] and not include_dirs:
                continue
            # aggregate results and crop the path to one level under dir_path
            result.append(
                blob[: len(blob_name)]
                + blob[len(blob_name) :].split("/", maxsplit=1)[0]
            )
        blobs = [self._blobname_to_azureuri(container_name, blob) for blob in result]
        return list(set(blobs))

    def exists(self, path: str) -> bool:
        container_name, blob_name = self._parse_url(path)
        container = self.client.get_container_client(container_name)
        blobs = list(container.list_blob_names(name_starts_with=blob_name))
        return len(blobs) > 0

    def is_dir(self, path: str) -> bool:
        path = path.rstrip("/") + "/"
        return self.exists(path)

    def is_file(self, path: str) -> bool:
        return self.exists(path) and not self.is_dir(path)

    def is_absolute(self, path: str) -> bool:
        return path.startswith(self.endpoint_protocol)

    def mkdir(
        self, dir_path: str, parents: bool = False, exist_ok: bool = False
    ) -> None:
        dir_path = dir_path.rstrip("/") + "/"
        if self.exists(dir_path) and not exist_ok:
            raise FileExistsError(f"Path {dir_path} already exists")
        parent = self.parent(dir_path)
        if not self.exists(parent) and not parents:
            raise FileNotFoundError(f"Path {parent} doesn't exist")
        self.dump_bytes(b"", dir_path)

    def remove_dir(self, dir_path: str) -> None:
        if not self.is_dir(dir_path):
            raise ValueError(f"Path is not a dir: {dir_path}")
        container_name, blob_name = self._parse_url(dir_path)
        blob_name = blob_name.rstrip("/") + "/"
        container = self.client.get_container_client(container_name)
        blob_names = list(container.list_blob_names(name_starts_with=blob_name))
        container.delete_blobs(*blob_names)

    def joinpath(self, dir_path: str, path: str) -> str:
        return dir_path.rstrip("/") + "/" + path.lstrip("/")

    def parents(self, path: str) -> List[str]:
        container_name, blob_name = self._parse_url(path)
        blob_name = blob_name.rstrip("/")
        blob_bits = blob_name.split("/")
        urls = []
        if len(blob_bits) == 1:
            urls.append(self._blobname_to_azureuri(container_name, ""))
        else:
            for index in range(len(blob_bits) - 1, -1, -1):
                parent = str.join("/", blob_bits[:index])
                urls.append(self._blobname_to_azureuri(container_name, parent))
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
        container_name = path_parts[0]
        blob_name = path_parts[1]
        return container_name, blob_name

    def _blobname_to_azureuri(self, container_name: str, blob_name: str) -> str:
        return f"{self.endpoint_protocol}://{self.account_name}.blob.{self.endpoint_suffix}/{container_name}/{blob_name}"

    def _get_blob(self, path: str) -> BlobClient:
        container_name, blob_name = self._parse_url(path)
        return self.client.get_container_client(container_name).get_blob_client(
            blob_name
        )

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
