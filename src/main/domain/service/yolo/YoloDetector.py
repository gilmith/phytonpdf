from abc import ABC, abstractmethod
from typing import List

from ultralytics.engine.results import Results


class YoloDetector(ABC):

    @abstractmethod
    def detect(self, imagen_bytes: bytes) -> List[Results]:
        pass

    @abstractmethod
    def train(self, bucket_name: str, file_name: str):
        pass

    @abstractmethod
    def analyze_resultset(self, resultset, file_name: str):
        pass