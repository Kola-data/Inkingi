from sqlalchemy import Column, String, Integer, ForeignKey, Text, DateTime, Boolean, JSON
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class Message(BaseModel):
    __tablename__ = "messages"
    
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=False)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    subject = Column(String(255), nullable=True)
    content = Column(Text, nullable=False)
    message_type = Column(String(20), nullable=False)  # email, sms, notification
    priority = Column(String(10), default="normal")  # low, normal, high, urgent
    status = Column(String(20), default="draft")  # draft, sent, failed, cancelled
    scheduled_at = Column(DateTime(timezone=True), nullable=True)
    sent_at = Column(DateTime(timezone=True), nullable=True)
    template_id = Column(String(100), nullable=True)
    metadata = Column(JSON, nullable=True)  # Additional data for templates
    
    # Relationships
    school = relationship("School")
    sender = relationship("User")
    recipients = relationship("MessageRecipient", back_populates="message")

class MessageRecipient(BaseModel):
    __tablename__ = "message_recipients"
    
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=False)
    message_id = Column(Integer, ForeignKey("messages.id"), nullable=False)
    recipient_type = Column(String(20), nullable=False)  # user, parent, student, staff
    recipient_id = Column(Integer, nullable=False)  # ID of the recipient entity
    email = Column(String(255), nullable=True)
    phone = Column(String(20), nullable=True)
    status = Column(String(20), default="pending")  # pending, sent, delivered, failed, read
    sent_at = Column(DateTime(timezone=True), nullable=True)
    delivered_at = Column(DateTime(timezone=True), nullable=True)
    read_at = Column(DateTime(timezone=True), nullable=True)
    error_message = Column(Text, nullable=True)
    
    # Relationships
    school = relationship("School")
    message = relationship("Message", back_populates="recipients")