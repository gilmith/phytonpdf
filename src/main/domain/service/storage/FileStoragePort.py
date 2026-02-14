from abc import ABC, abstractmethod
from pathlib import Path

from src.main.domain.model.FileInfo.FileInfoDom import FileInfoDom


class FileStoragePort(ABC):
    @abstractmethod
    def list_files(self, bucket_name: str) -> list[FileInfoDom]:
        """:return list of files in bucket"""
        pass
    @abstractmethod
    def insertData(self, bucket_name, file_name):
        """:return insert data from file in bucket"""
        pass

    @abstractmethod
    def get_file(self, bucket_name, file_name) -> bytes:
        """:return file from bucket"""
        pass

    @abstractmethod
    def upload_jpg(self, bucket_name, jpg_path: Path):
        pass