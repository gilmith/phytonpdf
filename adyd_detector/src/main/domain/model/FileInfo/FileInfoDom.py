from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from pydantic import Field

@dataclass
class FileInfoDom:
    file_name: str
    type_file: str
    content: bytes
    url: Optional[str] = None
    analyze_date: datetime = Field(default_factory=datetime.now)
    success: bool = False
