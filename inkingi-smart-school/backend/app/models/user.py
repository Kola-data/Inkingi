from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Table, Enum as SQLEnum, UniqueConstraint, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import BaseModel, TenantModel
import enum


class UserStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    DELETED = "deleted"


class RoleScope(str, enum.Enum):
    SYSTEM = "system"  # System-wide roles
    SCHOOL = "school"  # School-specific roles


class ScopeType(str, enum.Enum):
    SCHOOL = "school"
    CLASS = "class"
    COURSE = "course"


class User(TenantModel):
    __tablename__ = "users"
    __table_args__ = (
        UniqueConstraint("school_id", "email", name="uq_users_school_email"),
        Index("ix_users_email", "email"),
    )
    
    staff_id = Column(UUID(as_uuid=True), ForeignKey("staff.id"), nullable=True)
    email = Column(String(255), nullable=False)
    phone = Column(String(50), nullable=True)
    password_hash = Column(String(255), nullable=False)
    status = Column(SQLEnum(UserStatus), default=UserStatus.ACTIVE, nullable=False)
    
    # Authentication
    last_login_at = Column(DateTime(timezone=True), nullable=True)
    password_changed_at = Column(DateTime(timezone=True), nullable=True)
    failed_login_attempts = Column(String(5), default="0", nullable=False)
    locked_until = Column(DateTime(timezone=True), nullable=True)
    
    # Two-factor authentication
    two_factor_enabled = Column(Boolean, default=False, nullable=False)
    two_factor_secret = Column(String(255), nullable=True)
    
    # Profile
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    avatar_url = Column(String(500), nullable=True)
    preferences_json = Column(String, nullable=True)
    
    # Relationships
    staff = relationship("Staff", back_populates="user", uselist=False)
    roles = relationship("UserRole", back_populates="user", cascade="all, delete-orphan")
    access_controls = relationship("AccessControlEntry", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User {self.email}>"


class Role(BaseModel):
    __tablename__ = "roles"
    
    name = Column(String(50), unique=True, nullable=False)
    display_name = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)
    scope = Column(SQLEnum(RoleScope), default=RoleScope.SCHOOL, nullable=False)
    is_system = Column(Boolean, default=False, nullable=False)
    
    # Relationships
    permissions = relationship("RolePermission", back_populates="role", cascade="all, delete-orphan")
    users = relationship("UserRole", back_populates="role")
    
    def __repr__(self):
        return f"<Role {self.name}>"


class Permission(BaseModel):
    __tablename__ = "permissions"
    
    name = Column(String(100), unique=True, nullable=False)
    display_name = Column(String(200), nullable=False)
    description = Column(String(500), nullable=True)
    resource = Column(String(50), nullable=False)  # e.g., "school", "user", "class"
    action = Column(String(50), nullable=False)  # e.g., "create", "read", "update", "delete"
    
    # Relationships
    roles = relationship("RolePermission", back_populates="permission")
    
    def __repr__(self):
        return f"<Permission {self.name}>"


class RolePermission(BaseModel):
    __tablename__ = "role_permissions"
    __table_args__ = (
        UniqueConstraint("role_id", "permission_id", name="uq_role_permission"),
    )
    
    role_id = Column(UUID(as_uuid=True), ForeignKey("roles.id"), nullable=False)
    permission_id = Column(UUID(as_uuid=True), ForeignKey("permissions.id"), nullable=False)
    
    # Relationships
    role = relationship("Role", back_populates="permissions")
    permission = relationship("Permission", back_populates="roles")


class UserRole(TenantModel):
    __tablename__ = "user_roles"
    __table_args__ = (
        UniqueConstraint("user_id", "role_id", "school_id", name="uq_user_role_school"),
    )
    
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    role_id = Column(UUID(as_uuid=True), ForeignKey("roles.id"), nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="roles")
    role = relationship("Role", back_populates="users")


class AccessControlEntry(TenantModel):
    __tablename__ = "access_control_entries"
    __table_args__ = (
        Index("ix_ace_user_scope", "user_id", "scope_type", "scope_id"),
    )
    
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    scope_type = Column(SQLEnum(ScopeType), nullable=False)
    scope_id = Column(UUID(as_uuid=True), nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="access_controls")
    
    def __repr__(self):
        return f"<ACE {self.user_id} -> {self.scope_type}:{self.scope_id}>"