from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_async_session
from app.core.security import verify_password, get_password_hash, create_access_token, create_refresh_token
from app.models.user import User
from app.models.school import School
from app.schemas.auth import LoginRequest, LoginResponse, RegisterRequest, RegisterResponse, RefreshTokenRequest
from datetime import datetime
import uuid

router = APIRouter()


@router.post("/login", response_model=LoginResponse)
async def login(
    request: LoginRequest,
    db: AsyncSession = Depends(get_async_session)
):
    """Login with email and password"""
    # Find user by email and school
    query = select(User).where(User.email == request.email)
    if request.school_slug:
        # Get school by slug
        school_result = await db.execute(
            select(School).where(School.slug == request.school_slug)
        )
        school = school_result.scalar_one_or_none()
        if not school:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="School not found"
            )
        query = query.where(User.school_id == school.id)
    
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    
    # Verify user and password
    if not user or not verify_password(request.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Check user status
    if user.status != "active":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is not active"
        )
    
    # Update last login
    user.last_login_at = datetime.utcnow()
    await db.commit()
    
    # Create tokens
    token_data = {
        "sub": str(user.id),
        "email": user.email,
        "school_id": str(user.school_id)
    }
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)
    
    return LoginResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        user={
            "id": str(user.id),
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "school_id": str(user.school_id)
        }
    )


@router.post("/register", response_model=RegisterResponse)
async def register(
    request: RegisterRequest,
    db: AsyncSession = Depends(get_async_session)
):
    """Register a new school and admin user"""
    # Check if school slug is unique
    school_result = await db.execute(
        select(School).where(School.slug == request.school_slug)
    )
    if school_result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="School slug already exists"
        )
    
    # Check if email is unique
    email_result = await db.execute(
        select(User).where(User.email == request.email)
    )
    if email_result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create school
    school = School(
        id=uuid.uuid4(),
        name=request.school_name,
        slug=request.school_slug,
        contact_email=request.email,
        contact_phone=request.phone or "",
        address_json={
            "street": request.address,
            "city": request.city,
            "country": request.country
        },
        status="pending"
    )
    db.add(school)
    
    # Create admin user
    user = User(
        id=uuid.uuid4(),
        school_id=school.id,
        email=request.email,
        phone=request.phone,
        password_hash=get_password_hash(request.password),
        first_name=request.first_name,
        last_name=request.last_name,
        status="active"
    )
    db.add(user)
    
    await db.commit()
    await db.refresh(school)
    await db.refresh(user)
    
    return RegisterResponse(
        message="Registration successful. Your school is pending verification.",
        school={
            "id": str(school.id),
            "name": school.name,
            "slug": school.slug,
            "status": school.status
        },
        user={
            "id": str(user.id),
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name
        }
    )


@router.post("/refresh")
async def refresh_token(
    request: RefreshTokenRequest,
    db: AsyncSession = Depends(get_async_session)
):
    """Refresh access token using refresh token"""
    from app.core.security import decode_token
    
    # Decode refresh token
    payload = decode_token(request.refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    # Get user
    user_id = payload.get("sub")
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()
    
    if not user or user.status != "active":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive"
        )
    
    # Create new access token
    token_data = {
        "sub": str(user.id),
        "email": user.email,
        "school_id": str(user.school_id)
    }
    access_token = create_access_token(token_data)
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }