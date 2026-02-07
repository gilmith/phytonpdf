from abc import ABC


class PdfAnalizerPort(ABC):

    def has_ocr(self, file_name: str, file_bytes: bytes) -> bool:
        """Return True if file has ocr"""
        pass

    def analyze_header(self, file_name: str, file_bytes: bytes) -> str:
        """Return ocr text to insert"""