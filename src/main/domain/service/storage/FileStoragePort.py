from abc import ABC, abstractmethod

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