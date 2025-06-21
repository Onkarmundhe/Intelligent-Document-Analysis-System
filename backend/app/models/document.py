from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class DocumentUpload(BaseModel):
    filename: str
    content_type: str
    size: int

class DocumentResponse(BaseModel):
    id: str
    filename: str
    content_type: str
    size: int
    upload_date: datetime
    page_count: Optional[int] = None
    word_count: Optional[int] = None
    status: str = "processed"

class DocumentSummary(BaseModel):
    document_id: str
    summary: str
    key_points: List[str]
    word_count: int
    generated_at: datetime

class DocumentChunk(BaseModel):
    id: str
    document_id: str
    content: str
    page_number: Optional[int] = None
    chunk_index: int
    metadata: dict = {}

class DocumentComparison(BaseModel):
    document_ids: List[str]
    similarities: List[dict]
    differences: List[dict]
    common_themes: List[str] 