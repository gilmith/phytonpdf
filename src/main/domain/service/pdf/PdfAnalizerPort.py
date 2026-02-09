from abc import ABC, abstractmethod


class PdfAnalizerPort(ABC):

    @abstractmethod
    def has_ocr(self, file_name: str, file_bytes: bytes) -> bool:
        """Return True if file has ocr"""
        pass
    @abstractmethod
    def analyze_header(self, file_name: str, file_bytes: bytes) -> str:
        """Return ocr text to insert"""
    @abstractmethod
    def split_in_jpg(self, file_data: bytes, bucket_name: str, file_name: str):
        pass