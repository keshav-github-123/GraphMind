"""Pydantic models for request/response validation."""
from datetime import datetime
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field, validator

class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

class WebSocketMessageType(str, Enum):
    THREAD_ID = "thread_id"
    TOKEN = "token"
    STATUS = "status"
    COMPLETE = "complete"
    ERROR = "error"

class ChatMessageRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=10000)
    thread_id: Optional[str] = None

class Message(BaseModel):
    role: MessageRole
    content: str
    timestamp: Optional[datetime] = None

class ThreadSummary(BaseModel):
    thread_id: str
    summary: str
    created_at: str

class ThreadListResponse(BaseModel):
    threads: List[ThreadSummary]
    error: Optional[str] = None

class ChatHistoryResponse(BaseModel):
    messages: List[Message]
    error: Optional[str] = None

class DeleteThreadResponse(BaseModel):
    status: str
    message: Optional[str] = None
    error: Optional[str] = None

class FileUploadResponse(BaseModel):
    status: str
    filename: Optional[str] = None
    chunks_added: Optional[int] = None
    message: Optional[str] = None
