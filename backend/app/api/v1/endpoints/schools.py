from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from datetime import datetime

from app.core.database import get_db
from app.core.security import get_current_user, require_roles
from app.schemas.school import SchoolCreate, SchoolUpdate, SchoolResponse
from app.models.school import School
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=SchoolResponse)
async def create_school(
    school: SchoolCreate,
    db: AsyncSession = Depends(get_db)
):
    # Check if school with slug already exists
    result = await db.execute(select(School).where(School.slug == school.slug))
    existing_school = result.scalar_one_or_none()
    if existing_school:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="School with this slug already exists"
        )
    
    # Create new school
    db_school = School(
        name=school.name,
        slug=school.slug,
        contact_email=school.contact_email,
        contact_phone=school.contact_phone,
        address=school.address,
        website=school.website,
        description=school.description,
        tenant_id=0  # Will be updated after creation
    )
    
    db.add(db_school)
    await db.commit()
    await db.refresh(db_school)
    
    # Update tenant_id to match school id
    db_school.tenant_id = db_school.id
    await db.commit()
    
    return db_school

@router.get("/", response_model=List[SchoolResponse])
async def list_schools(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # System admin can see all schools, others only their own
    if current_user.school_id:
        result = await db.execute(select(School).where(School.id == current_user.school_id))
        schools = [result.scalar_one_or_none()]
    else:
        result = await db.execute(select(School).offset(skip).limit(limit))
        schools = result.scalars().all()
    
    return [school for school in schools if school]

@router.get("/{school_id}", response_model=SchoolResponse)
async def get_school(
    school_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(School).where(School.id == school_id))
    school = result.scalar_one_or_none()
    
    if not school:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="School not found"
        )
    
    # Check if user has access to this school
    if current_user.school_id and current_user.school_id != school_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this school"
        )
    
    return school

@router.put("/{school_id}", response_model=SchoolResponse)
async def update_school(
    school_id: int,
    school_update: SchoolUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(School).where(School.id == school_id))
    school = result.scalar_one_or_none()
    
    if not school:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="School not found"
        )
    
    # Check if user has access to this school
    if current_user.school_id and current_user.school_id != school_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this school"
        )
    
    # Update school fields
    update_data = school_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(school, field, value)
    
    await db.commit()
    await db.refresh(school)
    
    return school

@router.post("/{school_id}/verify")
async def verify_school(
    school_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles("system_admin"))
):
    result = await db.execute(select(School).where(School.id == school_id))
    school = result.scalar_one_or_none()
    
    if not school:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="School not found"
        )
    
    school.status = "active"
    school.verified_at = datetime.utcnow()
    
    await db.commit()
    
    return {"message": "School verified successfully"}