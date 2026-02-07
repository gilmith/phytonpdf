from dataclasses import dataclass


@dataclass
class FileInfoDom:
    file_name: str
    file_size: int
    unit: str
    content_type: str
    last_modified: str
    has_ocr: bool = False
