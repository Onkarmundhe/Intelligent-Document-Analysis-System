from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ChatQuestion(BaseModel):
    question: str
    document_ids: Optional[List[str]] = None
    include_sources: bool = True

class ChatSource(BaseModel):
    document_id: str
    document_name: str
    page_number: Optional[int] = None
    chunk_text: str
    relevance_score: float

class ChatResponse(BaseModel):
    question: str
    answer: str
    sources: List[ChatSource] = []
    response_time: float
    timestamp: datetime
    document_ids: List[str] = []

class ChatHistory(BaseModel):
    document_id: Optional[str] = None
    conversations: List[ChatResponse] = []
    total_questions: int = 0

class ChatRequest(BaseModel):
    question: str
    document_ids: Optional[List[str]] = None
    conversation_id: Optional[str] = None
    max_sources: int = 5 