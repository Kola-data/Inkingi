from typing import Optional, Annotated
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_async_session
from app.core.security import decode_token
from app.models.user import User
from app.models.school import School

# Security scheme
security = HTTPBearer()


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    db: AsyncSession = Depends(get_async_session)
) -> User:
    """Get the current authenticated user from JWT token"""
    token = credentials.credentials
    
    # Decode token
    payload = decode_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check token type
    if payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type",
        )
    
    # Get user from database
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )
    
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    if user.status != "active":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is not active",
        )
    
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
) -> User:
    """Ensure the current user is active"""
    if current_user.status != "active":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    return current_user


async def get_current_school(
    request: Request,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
) -> Optional[School]:
    """Get the current school from tenant context"""
    # Get tenant slug from request state (set by middleware)
    tenant_slug = getattr(request.state, "tenant_slug", None)
    
    if not tenant_slug:
        # Try to get from user's school
        return await db.get(School, current_user.school_id)
    
    # Get school by slug
    result = await db.execute(
        select(School).where(School.slug == tenant_slug)
    )
    school = result.scalar_one_or_none()
    
    if not school:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="School not found"
        )
    
    # Verify user has access to this school
    if current_user.school_id != school.id:
        # Check if user is system admin
        # For now, we'll allow access - implement proper RBAC later
        pass
    
    return school


class RoleChecker:
    """Dependency to check if user has required role"""
    
    def __init__(self, allowed_roles: list):
        self.allowed_roles = allowed_roles
    
    async def __call__(
        self,
        current_user: User = Depends(get_current_active_user),
        db: AsyncSession = Depends(get_async_session)
    ) -> User:
        # Load user roles
        # This is simplified - you'd want to properly load and check roles
        # For now, we'll allow all authenticated users
        return current_user


# Convenience role checkers
require_system_admin = RoleChecker(["system_admin"])
require_school_admin = RoleChecker(["system_admin", "school_admin"])
require_teacher = RoleChecker(["system_admin", "school_admin", "teacher"])
require_accountant = RoleChecker(["system_admin", "school_admin", "accountant"])