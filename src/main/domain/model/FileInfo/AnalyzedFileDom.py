from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class AnalyzedFileDom(BaseModel):
    monster_name: str
    url: Optional[str] = None
    analyze_date: datetime = Field(default_factory=datetime.now)
    success: bool = False