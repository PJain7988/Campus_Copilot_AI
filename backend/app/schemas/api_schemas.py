from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime

# --- Auth Schemas ---
class UserRegister(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    role: Optional[str] = "STUDENT"
    university_code: Optional[str] = "GU"

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: Dict[str, Any]

class UserProfile(BaseModel):
    id: str
    email: str
    full_name: str
    role: str
    university_id: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

# --- Chat & RAG Schemas ---
class ChatMessageRequest(BaseModel):
    conversation_id: Optional[str] = None
    message: str

class CitationItem(BaseModel):
    document_title: str
    page_number: int
    snippet: str
    relevance_score: float

class ChatMessageResponse(BaseModel):
    conversation_id: str
    message_id: str
    sender: str
    content: str
    intent_category: Optional[str] = None
    groundedness_score: Optional[float] = None
    citations: List[CitationItem] = []
    latency_ms: int = 0

class ConversationItem(BaseModel):
    id: str
    title: str
    created_at: datetime
    updated_at: datetime

# --- Document Schemas ---
class DocumentItem(BaseModel):
    id: str
    title: str
    file_type: str
    category: str
    version: str
    index_status: str
    total_pages: int
    created_at: datetime

    class Config:
        from_attributes = True

# --- Feedback Schemas ---
class FeedbackRequest(BaseModel):
    message_id: str
    rating: int  # 1 or -1
    comment: Optional[str] = None
