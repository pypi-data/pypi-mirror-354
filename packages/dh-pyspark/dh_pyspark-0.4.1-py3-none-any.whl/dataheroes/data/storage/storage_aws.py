import io
import os
import pathlib
from re import L
import shutil
import tempfile
from typing import Any, List, Tuple, Union
from urllib.parse import urlparse
from uuid import uuid4

import boto3
from botocore.exceptions import ClientError
from dataheroes.configuration import DataHeroesConfiguration
from dataheroes.data import helpers
from dataheroes.data.storage.storage import Storage


class StorageAWS(Storage):
    def __init__(self):
        config = DataHeroesConfiguration()
        access_key_id = config.get_param(name="access_key_id", section="aws")
        secret_access_key = config.get_param(name="secret_access_key", section="aws")
        region = config.get_param(name="region", section="aws")
        try:
            self.client = boto3.client(
                "s3",
                aws_access_key_id=access_key_id,
                aws_secret_access_key=secret_access_key,
                region_name=region,
            )
        except Exception as e:
            msg = (
                "Exception while creating S3 client. Check DataHeroes config file"
                + "or use the dataheroes.cli script to configure credentials for AWS S3.\n"
            )
            msg += str(e)
            raise Exception(msg) from e

    def read_bytes(self, storage_path: str, local_copy_dir: str = None) -> io.BytesIO:
        do_cleanup = local_copy_dir is None
        local_copy_dir = local_copy_dir or tempfile.TemporaryDirectory().name
        # For S3, downloading data to a file is faster than directly loading bytes
        _, obj_key = self._parse_url(storage_path)
        local_path = pathlib.Path(local_copy_dir, obj_key)
        if not local_path.exists():
            local_path.parent.mkdir(parents=True, exist_ok=True)
            self.storage_to_local(storage_path, str(local_path))
        data = helpers.localpath_to_bytestream(local_path)
        if do_cleanup:
            shutil.rmtree(local_copy_dir)
        return data

    def dump_bytes(self, data: bytes, storage_path: str) -> str:
        bucket, object_key = self._parse_url(storage_path)
        # upload_file() is much faster than put_object()
        # so we save the data in a temporary file which we use for the upload
        with tempfile.TemporaryFile("wb+") as f:
            f.write(data)
            f.seek(0)
            self.client.upload_fileobj(f, bucket, object_key)
        return storage_path

    def local_to_storage(
        self, local_path: Union[str, os.PathLike], storage_path: str
    ) -> str:
        bucket, object_key = self._parse_url(storage_path)
        self.client.upload_file(local_path, bucket, object_key)
        return storage_path

    def storage_to_local(
        self, storage_path: str, local_path: Union[str, os.PathLike]
    ) -> str:
        if not self.is_file(storage_path):
            raise FileNotFoundError(
                f"Path {storage_path} doesn't exist or is a directory."
            )
        bucket, obj_key = self._parse_url(storage_path)
        local_path = pathlib.Path(local_path)
        if not local_path.exists():
            local_path.parent.mkdir(parents=True, exist_ok=True)
            self.client.download_file(bucket, obj_key, local_path)
        return str(local_path)

    def iterdir(self, dir_path: str, include_dirs: bool = False) -> List[str]:
        if not self.exists(dir_path):
            raise FileNotFoundError(f"Path {dir_path} could not be found")
        if self.is_file(dir_path):
            return [dir_path]
        bucket_name, obj_key = self._parse_url(dir_path)
        response = self.client.list_objects_v2(Bucket=bucket_name, Prefix=obj_key)
        sub_objects = []

        if "Contents" not in response.keys():
            raise FileNotFoundError(
                f"Path: {dir_path} could not be found."
            )

        sub_objects = [obj["Key"] for obj in response["Contents"]]
        result = []
        # add the trailing '/' to dir_path
        obj_key = obj_key.rstrip("/") + "/"
        for obj in sub_objects:
            # remove self-referential result
            if obj == obj_key:
                continue
            # remove other files or dirs with the same prefix
            if obj[len(obj_key) - 1] != "/":
                continue
            # remove subdirs if include_dirs == False
            if "/" in obj[len(obj_key) :] and not include_dirs:
                continue
            # aggregate results and crop the path to one level under dir_path
            result.append(
                obj[: len(obj_key)] + obj[len(obj_key) :].split("/", maxsplit=1)[0]
            )

        sub_uris = [self._objkey_to_s3url(obj, bucket_name) for obj in result]
        return list(set(sub_uris))

    def exists(self, path: str) -> bool:
        bucket_name, obj_key = self._parse_url(path)
        response = self.client.list_objects_v2(Bucket=bucket_name, Prefix=obj_key)
        return "Contents" in response

    def is_dir(self, path: str) -> bool:
        path = path.rstrip("/") + "/"
        return self.exists(path)

    def is_file(self, path: str) -> bool:
        return self.exists(path) and not self.is_dir(path)

    def is_absolute(self, path: str) -> bool:
        return path.startswith("s3://")

    def mkdir(
        self, dir_path: str, parents: bool = False, exist_ok: bool = False
    ) -> None:
        dir_path = dir_path.rstrip("/") + "/"
        if self.exists(dir_path) and not exist_ok:
            raise FileExistsError(f"Path {dir_path} already exists")
        parent = self.parent(dir_path)
        if not self.exists(parent) and not parents:
            raise FileNotFoundError(f"Path {parent} doesn't exist")
        bucket_name, obj_key = self._parse_url(dir_path)
        self.client.put_object(Bucket=bucket_name, Key=obj_key)

    def remove_dir(self, path: str) -> None:
        if not self.is_dir(path):
            raise ValueError(f"Path is not a dir: {path}")
        bucket_name, obj_key = self._parse_url(path)
        obj_key = obj_key.rstrip("/") + "/"
        response = self.client.list_objects_v2(Bucket=bucket_name, Prefix=obj_key)
        objects = [{"Key": obj["Key"]} for obj in response.get("Contents", [])]
        self.client.delete_objects(Bucket=bucket_name, Delete={"Objects": objects})

    def joinpath(self, dir_path: str, obj_key: str) -> str:
        return dir_path.rstrip("/") + "/" + obj_key.lstrip("/")

    def parents(self, path: str) -> List[str]:
        bucket_name, obj_key = self._parse_url(path)
        obj_key = obj_key.rstrip("/")
        key_bits = obj_key.split("/")
        urls = []
        if len(key_bits) == 1:
            urls.append(self._objkey_to_s3url("", bucket_name))
        else:
            for index in range(len(key_bits) - 1, -1, -1):
                parent = str.join("/", key_bits[:index])
                urls.append(self._objkey_to_s3url(parent, bucket_name))
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
        bucket_name = parsed_url.netloc
        object_name = parsed_url.path.lstrip("/")

        return bucket_name, object_name

    def _objkey_to_s3url(self, obj_key: str, bucket_name: str) -> str:
        return f"s3://{bucket_name}/{obj_key}"
