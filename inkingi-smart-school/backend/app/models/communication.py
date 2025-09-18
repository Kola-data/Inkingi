from sqlalchemy import Column, String, Text, ForeignKey, DateTime, Enum as SQLEnum, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import TenantModel
import enum


class MessageType(str, enum.Enum):
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"
    IN_APP = "in_app"


class MessageStatus(str, enum.Enum):
    DRAFT = "draft"
    QUEUED = "queued"
    SENDING = "sending"
    SENT = "sent"
    FAILED = "failed"
    DELIVERED = "delivered"
    READ = "read"


class NotificationType(str, enum.Enum):
    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"
    ANNOUNCEMENT = "announcement"
    REMINDER = "reminder"
    ALERT = "alert"


class Message(TenantModel):
    __tablename__ = "messages"
    
    # Message details
    message_type = Column(SQLEnum(MessageType), nullable=False)
    subject = Column(String(500), nullable=True)
    content = Column(Text, nullable=False)
    
    # Sender
    sender_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    sender_name = Column(String(200), nullable=True)
    sender_email = Column(String(255), nullable=True)
    
    # Recipients (JSON arrays)
    to_users = Column(JSON, nullable=True)  # Array of user IDs
    to_emails = Column(JSON, nullable=True)  # Array of email addresses
    to_phones = Column(JSON, nullable=True)  # Array of phone numbers
    to_groups = Column(JSON, nullable=True)  # Array of group identifiers (e.g., "all_teachers", "class_p1")
    
    # Status tracking
    status = Column(SQLEnum(MessageStatus), default=MessageStatus.DRAFT, nullable=False)
    scheduled_at = Column(DateTime(timezone=True), nullable=True)
    sent_at = Column(DateTime(timezone=True), nullable=True)
    
    # Delivery tracking (JSON)
    delivery_report = Column(JSON, nullable=True)
    failed_recipients = Column(JSON, nullable=True)
    
    # Attachments (JSON array)
    attachments = Column(JSON, nullable=True)
    
    # Template
    template_id = Column(String(100), nullable=True)
    template_variables = Column(JSON, nullable=True)
    
    def __repr__(self):
        return f"<Message {self.message_type} - {self.subject}>"


class Notification(TenantModel):
    __tablename__ = "notifications"
    
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    notification_type = Column(SQLEnum(NotificationType), nullable=False)
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    
    # Action link
    action_url = Column(String(500), nullable=True)
    action_text = Column(String(100), nullable=True)
    
    # Status
    is_read = Column(String, default="false", nullable=False)
    read_at = Column(DateTime(timezone=True), nullable=True)
    
    # Metadata
    metadata = Column(JSON, nullable=True)
    
    # Expiry
    expires_at = Column(DateTime(timezone=True), nullable=True)
    
    def __repr__(self):
        return f"<Notification {self.user_id} - {self.title}>"