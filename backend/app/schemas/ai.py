from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class ChatSessionBase(BaseModel):
    title: Optional[str] = None
    context: Optional[Dict[str, Any]] = None

class ChatSessionCreate(ChatSessionBase):
    pass

class ChatSessionUpdate(BaseModel):
    title: Optional[str] = None
    status: Optional[str] = None
    context: Optional[Dict[str, Any]] = None

class ChatSessionResponse(ChatSessionBase):
    id: int
    school_id: int
    user_id: int
    status: str
    last_message_at: Optional[datetime]
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True

class ChatMessageBase(BaseModel):
    role: str
    content: str
    metadata: Optional[Dict[str, Any]] = None

class ChatMessageCreate(ChatMessageBase):
    session_id: int

class ChatMessageResponse(ChatMessageBase):
    id: int
    school_id: int
    session_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True