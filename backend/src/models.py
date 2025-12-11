"""Pydantic models."""
from typing import Literal, Optional, List
from pydantic import BaseModel
from datetime import datetime


class ConversationMessage(BaseModel):
    """Conversation message."""
    role: Literal['user', 'assistant', 'system']
    content: str
    timestamp: float


class SessionState(BaseModel):
    """Session state."""
    session_id: str
    conversation_history: List[ConversationMessage] = []
    current_phase: Literal['FASE_1', 'FASE_2', 'FASE_3'] = 'FASE_1'
    uc_validated: bool = False
    uc_number: Optional[str] = None
    start_time: float


class TokenRequest(BaseModel):
    """Token request."""
    room_name: str
    participant_name: str


class TokenResponse(BaseModel):
    """Token response."""
    token: str
    url: str


class SessionStartRequest(BaseModel):
    """Session start request."""
    session_id: str
    room_name: str


class SessionResponse(BaseModel):
    """Session response."""
    session_id: str
    status: str
    phase: Optional[str] = None
    uc_validated: Optional[bool] = None
    message_count: Optional[int] = None
    uptime: Optional[float] = None


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    timestamp: str
    active_sessions: int


class STTResult(BaseModel):
    """STT result."""
    transcript: str
    is_final: bool
    confidence: Optional[float] = None


class LLMResponse(BaseModel):
    """LLM response."""
    text: str
    metadata: Optional[dict] = None
