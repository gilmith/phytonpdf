from dataclasses import dataclass


@dataclass
class FileInfoStorageDom:
    file_name: str
    file_size: int
    unit: str
    content_type: str
    last_modified: str
