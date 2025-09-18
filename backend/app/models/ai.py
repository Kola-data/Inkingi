from sqlalchemy import Column, String, Integer, ForeignKey, Text, DateTime, Boolean, JSON
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class ChatSession(BaseModel):
    __tablename__ = "chat_sessions"
    
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=True)
    status = Column(String(20), default="active")  # active, archived, deleted
    context = Column(JSON, nullable=True)  # Additional context for the AI
    last_message_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    school = relationship("School")
    user = relationship("User")
    messages = relationship("ChatMessage", back_populates="session")

class ChatMessage(BaseModel):
    __tablename__ = "chat_messages"
    
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=False)
    session_id = Column(Integer, ForeignKey("chat_sessions.id"), nullable=False)
    role = Column(String(20), nullable=False)  # user, assistant, system
    content = Column(Text, nullable=False)
    metadata = Column(JSON, nullable=True)  # Additional data like sources, confidence, etc.
    created_at = Column(DateTime(timezone=True), nullable=False)
    
    # Relationships
    school = relationship("School")
    session = relationship("ChatSession", back_populates="messages")