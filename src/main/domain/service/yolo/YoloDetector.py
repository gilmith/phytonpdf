from abc import ABC, abstractmethod


class YoloDetector(ABC):

    @abstractmethod
    def detect(self, imagenbytes: bytes):
        pass

    @abstractmethod
    def train(self, bucket_name: str, file_name: str):
        pass