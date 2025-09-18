from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..db.session import Base
import enum


class MessageChannel(str, enum.Enum):
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"
    IN_APP = "in_app"


class MessageStatus(str, enum.Enum):
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    SENDING = "sending"
    SENT = "sent"
    DELIVERED = "delivered"
    FAILED = "failed"
    CANCELLED = "cancelled"


class RecipientType(str, enum.Enum):
    USER = "user"
    STAFF = "staff"
    STUDENT = "student"
    PARENT = "parent"
    CLASS = "class"
    ROLE = "role"
    ALL_STAFF = "all_staff"
    ALL_STUDENTS = "all_students"
    ALL_PARENTS = "all_parents"


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, nullable=False, index=True)
    
    # Message content
    subject = Column(String(255), nullable=True)  # For email, optional for SMS
    body = Column(Text, nullable=False)
    channel = Column(Enum(MessageChannel), nullable=False)
    
    # Sender information
    sender_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    sender_name = Column(String(255), nullable=True)  # Override sender display name
    sender_email = Column(String(255), nullable=True)  # Override sender email
    sender_phone = Column(String(100), nullable=True)  # Override sender phone
    
    # Recipient targeting
    recipient_scope = Column(String(50), nullable=False)  # individual, group, broadcast
    recipient_filter = Column(Text, nullable=True)  # JSON filter criteria
    
    # Scheduling
    scheduled_at = Column(DateTime(timezone=True), nullable=True)
    send_immediately = Column(Boolean, default=True, nullable=False)
    
    # Status and tracking
    status = Column(Enum(MessageStatus), nullable=False, default=MessageStatus.DRAFT)
    total_recipients = Column(Integer, nullable=False, default=0)
    sent_count = Column(Integer, nullable=False, default=0)
    delivered_count = Column(Integer, nullable=False, default=0)
    failed_count = Column(Integer, nullable=False, default=0)
    
    # Metadata
    message_type = Column(String(100), nullable=True)  # announcement, reminder, alert, etc.
    priority = Column(String(20), nullable=False, default="normal")  # low, normal, high, urgent
    tags = Column(Text, nullable=True)  # JSON array of tags
    
    # Timestamps
    sent_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    sender = relationship("User")
    recipients = relationship("MessageRecipient", back_populates="message", cascade="all, delete-orphan")
    attachments = relationship("MessageAttachment", back_populates="message", cascade="all, delete-orphan")


class MessageRecipient(Base):
    __tablename__ = "message_recipients"

    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, nullable=False, index=True)
    message_id = Column(Integer, ForeignKey('messages.id'), nullable=False, index=True)
    
    # Recipient identification
    recipient_type = Column(Enum(RecipientType), nullable=False)
    recipient_id = Column(Integer, nullable=True, index=True)  # ID of user/staff/student/parent
    recipient_email = Column(String(255), nullable=True)
    recipient_phone = Column(String(100), nullable=True)
    recipient_name = Column(String(255), nullable=True)
    
    # Delivery status
    status = Column(Enum(MessageStatus), nullable=False, default=MessageStatus.SENT)
    delivery_status = Column(String(50), nullable=True)  # Provider-specific status
    error_message = Column(Text, nullable=True)
    
    # Delivery tracking
    sent_at = Column(DateTime(timezone=True), nullable=True)
    delivered_at = Column(DateTime(timezone=True), nullable=True)
    opened_at = Column(DateTime(timezone=True), nullable=True)  # For email tracking
    clicked_at = Column(DateTime(timezone=True), nullable=True)  # For link tracking
    
    # Provider tracking
    provider_message_id = Column(String(255), nullable=True)  # External message ID
    provider_status = Column(String(100), nullable=True)  # Provider-specific status
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    message = relationship("Message", back_populates="recipients")


class MessageTemplate(Base):
    __tablename__ = "message_templates"

    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    
    # Template content
    subject_template = Column(String(255), nullable=True)
    body_template = Column(Text, nullable=False)
    channel = Column(Enum(MessageChannel), nullable=False)
    
    # Template metadata
    template_type = Column(String(100), nullable=True)  # welcome, reminder, alert, etc.
    variables = Column(Text, nullable=True)  # JSON array of template variables
    
    # Status
    is_active = Column(Boolean, default=True, nullable=False)
    is_system = Column(Boolean, default=False, nullable=False)  # System vs user-created
    
    # Metadata
    created_by = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    creator = relationship("User")


class MessageAttachment(Base):
    __tablename__ = "message_attachments"

    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, nullable=False, index=True)
    message_id = Column(Integer, ForeignKey('messages.id'), nullable=False, index=True)
    
    # File information
    filename = Column(String(255), nullable=False)
    original_filename = Column(String(255), nullable=False)
    file_size = Column(Integer, nullable=False)
    content_type = Column(String(100), nullable=False)
    file_path = Column(String(500), nullable=False)  # Storage path
    
    # Upload metadata
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    message = relationship("Message", back_populates="attachments")


class MessageLog(Base):
    __tablename__ = "message_logs"

    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, nullable=False, index=True)
    message_id = Column(Integer, ForeignKey('messages.id'), nullable=True, index=True)
    recipient_id = Column(Integer, ForeignKey('message_recipients.id'), nullable=True, index=True)
    
    # Log details
    event_type = Column(String(50), nullable=False)  # sent, delivered, opened, clicked, failed
    event_data = Column(Text, nullable=True)  # JSON data
    provider_response = Column(Text, nullable=True)  # Raw provider response
    
    # Timestamp
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    message = relationship("Message")
    recipient = relationship("MessageRecipient") 