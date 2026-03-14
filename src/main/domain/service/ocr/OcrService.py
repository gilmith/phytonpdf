from abc import ABC, abstractmethod


class OcrService(ABC):

    @abstractmethod
    def analyze_nombre(self, image_bytes: bytes) -> str:
        pass