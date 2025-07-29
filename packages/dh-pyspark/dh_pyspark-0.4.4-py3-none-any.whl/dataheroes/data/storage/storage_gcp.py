import io
import os
import pathlib
from typing import List, Tuple, Union
from urllib.parse import urlparse
from dataheroes.configuration import DataHeroesConfiguration
from dataheroes.data import helpers
from dataheroes.data.storage.storage import Storage
from google.cloud import storage
from google.cloud.storage.blob import Blob
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

class StorageGCP(Storage):
    def __init__(self):
        config = DataHeroesConfiguration()
        project_id = config.get_param(name="project_id", section="gcp")
        credentials_path = config.get_param(name="credentials_path", section="gcp")
        credentials = Credentials.from_authorized_user_file(credentials_path)
        try:
            self.client = storage.Client(project=project_id, credentials=credentials)
        except Exception as e:
            msg = "Exception while creating GCP storage client. Check DataHeroes config file" + \
                  "or use the dataheroes.cli script to configure credentials for GCP storage.\n"
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
        data = blob.download_as_bytes()
        return helpers.bytes_to_bytestream(data)

    def iterdir(self, dir_path, include_dirs=False) -> List[str]:
        if not self.exists(dir_path):
            raise FileNotFoundError(f"Path {dir_path} could not be found")
        if self.is_file(dir_path):
            return [dir_path]
        bucket_name, blob_name = self._parse_url(dir_path)
        bucket = self.client.bucket(bucket_name)

        blobs = list(bucket.list_blobs(prefix=blob_name))
        result = []
        blob_name = blob_name.rstrip("/") + "/"
        for blob in blobs:
            # remove self-referential result
            if blob.name == blob_name:
                continue
            # remove other files or dirs with the same prefix
            if blob.name[len(blob_name) - 1] != "/":
                continue
            # remove subdirs if include_dirs == False
            if "/" in blob.name[len(blob_name) :] and not include_dirs:
                continue
            # aggregate results and crop the path to one level under dir_path
            result.append(
                blob.name[: len(blob_name)]
                + blob.name[len(blob_name) :].split("/", maxsplit=1)[0]
            )
        blob_names = [self._blobname_to_gcpurl(blob, bucket_name) for blob in result]
        return list(set(blob_names))

    def local_to_storage(
        self, local_path: Union[str, os.PathLike], storage_path: str
    ) -> str:
        blob = self._create_blob(storage_path)
        blob.upload_from_filename(local_path)
        return storage_path

    def storage_to_local(
        self, storage_path: str, local_path: Union[str, os.PathLike]
    ) -> str:
        if not self.is_file(storage_path):
            raise FileNotFoundError(
                f"Path {storage_path} doesn't exist or is a directory"
            )
        local_path = pathlib.Path(local_path)
        if not local_path.exists():
            local_path.parent.mkdir(parents=True, exist_ok=True)
            blob = self._get_blob(storage_path)
            blob.download_to_filename(str(local_path))
        return str(local_path)
    
    def dump_bytes(self, data: bytes, storage_path: str) -> str:
        blob = self._create_blob(storage_path)
        blob.upload_from_string(data)

    def exists(self, path: str) -> bool:
        bucket_name, blob_name = self._parse_url(path)
        blobs = list(self.client.list_blobs(bucket_name, prefix=blob_name, max_results=1))
        return len(blobs) > 0

    def is_dir(self, path: str) -> bool:
        path = path.rstrip("/") + "/"
        return self.exists(path)

    def is_file(self, path: str) -> bool:
        return self.exists(path) and not self.is_dir(path)
    
    def stem(self, path: str) -> str:
        return self.name(path).rsplit(".", maxsplit=1)[0]

    def name(self, path: str) -> str:
        return path.rstrip("/").split("/")[-1]

    def parents(self, path: str) -> List[str]:
        bucket_name, blob_name = self._parse_url(path)
        blob_name = blob_name.rstrip("/")
        blob_bits = blob_name.split("/")
        urls = []
        if len(blob_bits) == 1:
            urls.append(self._blobname_to_gcpurl("", bucket_name))
        else:
            for index in range(len(blob_bits) - 1, -1, -1):
                parent = str.join("/", blob_bits[:index])
                urls.append(self._blobname_to_gcpurl(parent, bucket_name))
        # this adds the / that indicates a directory and avoid // for the root bucket path
        urls = [url.rstrip("/") + "/" for url in urls]
        return urls
    
    def parent(self, path: str) -> str:
        return self.parents(path)[0]
        
    def joinpath(self, dir_path: str, blob_name: str):
        return dir_path.rstrip("/") + "/" + blob_name.lstrip("/")

    def mkdir(self, dir_path: str, parents: bool = False, exist_ok: bool = False) -> None:
        dir_path = dir_path.rstrip("/") + "/"
        if self.exists(dir_path) and not exist_ok:
            raise FileExistsError(f"Path {dir_path} already exists")
        parent = self.parent(dir_path)
        if not self.exists(parent) and not parents:
            raise FileNotFoundError(f"Path {parent} doesn't exist")
        self.dump_bytes(b"", dir_path)

    def remove_dir(self, path: str) -> None:
        if not self.is_dir(path):
            raise ValueError(f"Path is not a dir: {path}")
        bucket_name, blob_name = self._parse_url(path)
        blob_name = blob_name.rstrip("/") + "/"
        bucket = self.client.get_bucket(bucket_name)
        bucket.delete_blobs(list(bucket.list_blobs(prefix=blob_name)))

    def is_absolute(self, path: str) -> bool:
        return path.startswith("gs://")

    def _parse_url(self, path: str) -> Tuple[str, str]:
        parsed_url = urlparse(path)
        bucket_name = parsed_url.netloc
        blob_name = parsed_url.path.lstrip('/')
        return bucket_name, blob_name

    def _blobname_to_gcpurl(self, blob_name: str, bucket_name: str) -> str:
        return f"gs://{bucket_name}/{blob_name}"

    def _create_blob(self, path: str) -> Blob:
        bucket_name, blob_name = self._parse_url(path)
        bucket = self.client.get_bucket(bucket_name)
        return bucket.blob(blob_name)

    def _get_blob(self, path: str) -> Blob:
        bucket_name, blob_name = self._parse_url(path)
        bucket = self.client.get_bucket(bucket_name)
        return bucket.get_blob(blob_name)
