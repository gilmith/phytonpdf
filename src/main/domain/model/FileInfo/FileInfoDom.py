from dataclasses import dataclass


@dataclass
class FileInfoDom:
    file_name: str
    type: str
    url: str
    success: bool
    content: bytes