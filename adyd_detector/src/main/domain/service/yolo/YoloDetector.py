from abc import ABC, abstractmethod
from typing import List

from ultralytics.engine.results import Results

from main.domain.model.yolo.DetectDom import DetectDom


class YoloDetector(ABC):

    @abstractmethod
    def detect(self, imagen_bytes: bytes, detect_dom: DetectDom) -> List[Results]:
        pass

    @abstractmethod
    def train(self, bucket_name: str, file_name: str):
        pass

    @abstractmethod
    def analyze_resultset(self, resultset, file_name: str):
        pass