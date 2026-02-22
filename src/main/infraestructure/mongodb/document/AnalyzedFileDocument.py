from pydantic import Field
from datetime import datetime
from beanie import Document


class AnalyzedFileDocument(Document):
    file_name: str
    type: str
    url: str
    analyze_date: datetime = Field(default_factory=datetime.now)
    success: bool

