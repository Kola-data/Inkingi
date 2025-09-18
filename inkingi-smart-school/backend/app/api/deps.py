"""
API dependencies
"""
from typing import Optional
from fastapi import Depends, HTTPException, status, Request
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.db.session import get_db, set_tenant_context
from app.models.user import User
from app.services.user import UserService


def get_current_user(
    request: Request,
    db: Session = Depends(get_db)
) -> User:
    """Get current authenticated user"""
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = auth_header.split(" ")[1]
    payload = decode_access_token(token)
    
    user_id = payload.get("sub")
    tenant_id = payload.get("tenant_id")
    
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Set tenant context if available
    if tenant_id:
        set_tenant_context(db, tenant_id)
    
    user_service = UserService()
    user = user_service.get_user_by_id(db, int(user_id))
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if user.status != "active":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account is not active",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user


def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """Get current active user"""
    return current_user


def get_tenant_id(request: Request) -> Optional[int]:
    """Get tenant ID from request state"""
    return getattr(request.state, 'tenant_id', None)


def require_tenant(
    request: Request,
    db: Session = Depends(get_db)
) -> int:
    """Require tenant context"""
    tenant_id = get_tenant_id(request)
    if not tenant_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tenant context required"
        )
    
    # Set tenant context for database queries
    set_tenant_context(db, tenant_id)
    return tenant_id