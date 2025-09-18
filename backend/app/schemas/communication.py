from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any, List
from datetime import datetime

class MessageBase(BaseModel):
    subject: Optional[str] = None
    content: str
    message_type: str
    priority: str = "normal"

class MessageCreate(MessageBase):
    recipients: List[Dict[str, Any]]
    scheduled_at: Optional[datetime] = None
    template_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class MessageResponse(MessageBase):
    id: int
    school_id: int
    sender_id: int
    status: str
    scheduled_at: Optional[datetime]
    sent_at: Optional[datetime]
    template_id: Optional[str]
    metadata: Optional[Dict[str, Any]]
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True