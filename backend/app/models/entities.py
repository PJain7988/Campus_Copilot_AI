from datetime import datetime, timezone
import uuid
from typing import List, Optional
from sqlalchemy import (
    Column, String, Text, Integer, Boolean, DateTime, ForeignKey, Float, JSON
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

def generate_uuid() -> str:
    return str(uuid.uuid4())

class University(Base):
    __tablename__ = "universities"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    code = Column(String(20), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    domain = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    users = relationship("User", back_populates="university")
    documents = relationship("Document", back_populates="university")


class User(Base):
    __tablename__ = "users"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    university_id = Column(String(36), ForeignKey("universities.id"), nullable=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    role = Column(String(50), default="STUDENT")  # STUDENT, STAFF, ADMIN
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    university = relationship("University", back_populates="users")
    conversations = relationship("Conversation", back_populates="user")
    feedback = relationship("Feedback", back_populates="user")


class Document(Base):
    __tablename__ = "documents"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    university_id = Column(String(36), ForeignKey("universities.id"), nullable=True)
    title = Column(String(255), nullable=False)
    file_path = Column(String(512), nullable=False)
    file_type = Column(String(50), default="PDF")
    category = Column(String(100), default="ACADEMIC")  # ACADEMIC, EXAM, FEES, PLACEMENT, GENERAL
    version = Column(String(50), default="1.0")
    index_status = Column(String(50), default="PENDING")  # PENDING, INDEXING, READY, FAILED
    total_pages = Column(Integer, default=1)
    published_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    university = relationship("University", back_populates="documents")
    chunks = relationship("DocumentChunk", back_populates="document", cascade="all, delete-orphan")


class DocumentChunk(Base):
    __tablename__ = "document_chunks"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    document_id = Column(String(36), ForeignKey("documents.id"), nullable=False)
    chunk_index = Column(Integer, nullable=False)
    page_number = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    embedding = Column(JSON, nullable=True)  # JSON vector array for universal compatibility
    metadata_json = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    document = relationship("Document", back_populates="chunks")


class Conversation(Base):
    __tablename__ = "conversations"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    title = Column(String(255), default="New University Query")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")


class Message(Base):
    __tablename__ = "messages"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    conversation_id = Column(String(36), ForeignKey("conversations.id"), nullable=False)
    sender = Column(String(20), nullable=False)  # USER, ASSISTANT, SYSTEM
    content = Column(Text, nullable=False)
    intent_category = Column(String(50), nullable=True)
    groundedness_score = Column(Float, nullable=True)
    latency_ms = Column(Integer, default=0)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    conversation = relationship("Conversation", back_populates="messages")
    citations = relationship("Citation", back_populates="message", cascade="all, delete-orphan")
    feedback = relationship("Feedback", back_populates="message", uselist=False)


class Citation(Base):
    __tablename__ = "citations"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    message_id = Column(String(36), ForeignKey("messages.id"), nullable=False)
    document_title = Column(String(255), nullable=False)
    page_number = Column(Integer, nullable=False)
    snippet = Column(Text, nullable=False)
    relevance_score = Column(Float, default=1.0)

    message = relationship("Message", back_populates="citations")


class Feedback(Base):
    __tablename__ = "feedback"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    message_id = Column(String(36), ForeignKey("messages.id"), nullable=False)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    rating = Column(Integer, nullable=False)  # 1 for helpful, -1 for not helpful
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    message = relationship("Message", back_populates="feedback")
    user = relationship("User", back_populates="feedback")


class CampusNotice(Base):
    __tablename__ = "campus_notices"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    title = Column(String(255), nullable=False)
    category = Column(String(100), default="ACADEMIC")
    summary = Column(Text, nullable=False)
    priority = Column(String(20), default="NORMAL")  # HIGH, NORMAL, LOW
    event_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
