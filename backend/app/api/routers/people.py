from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from ...api.deps import get_db, get_tenant_school_id
from ...models.school import Staff, Student, Parent, ParentStudent
from ...core.rbac import Permission, require_permission, UserRole

router = APIRouter()

# Staff endpoints
@router.post("/staff")
async def create_staff(
    staff_data: dict,
    db: AsyncSession = Depends(get_db),
    school_id: int = Depends(get_tenant_school_id),
):
    staff = Staff(
        school_id=school_id,
        first_name=staff_data["first_name"],
        last_name=staff_data["last_name"],
        email=staff_data.get("email"),
        phone=staff_data.get("phone"),
        position=staff_data.get("position"),
        status="active"
    )
    db.add(staff)
    await db.commit()
    await db.refresh(staff)
    return staff


@router.get("/staff")
async def list_staff(
    db: AsyncSession = Depends(get_db),
    school_id: int = Depends(get_tenant_school_id),
):
    result = await db.execute(
        select(Staff).where(Staff.school_id == school_id, Staff.status == "active")
    )
    return result.scalars().all()


# Student endpoints
@router.post("/students")
async def create_student(
    student_data: dict,
    db: AsyncSession = Depends(get_db),
    school_id: int = Depends(get_tenant_school_id),
):
    student = Student(
        school_id=school_id,
        first_name=student_data["first_name"],
        last_name=student_data["last_name"],
        admission_no=student_data.get("admission_no"),
        status="active"
    )
    db.add(student)
    await db.commit()
    await db.refresh(student)
    return student


@router.get("/students")
async def list_students(
    db: AsyncSession = Depends(get_db),
    school_id: int = Depends(get_tenant_school_id),
):
    result = await db.execute(
        select(Student).where(Student.school_id == school_id, Student.status == "active")
    )
    return result.scalars().all()


# Parent endpoints
@router.post("/parents")
async def create_parent(
    parent_data: dict,
    db: AsyncSession = Depends(get_db),
    school_id: int = Depends(get_tenant_school_id),
):
    parent = Parent(
        school_id=school_id,
        first_name=parent_data["first_name"],
        last_name=parent_data["last_name"],
        phone=parent_data.get("phone"),
        email=parent_data.get("email"),
        occupation=parent_data.get("occupation")
    )
    db.add(parent)
    await db.commit()
    await db.refresh(parent)
    return parent


@router.post("/parents/{parent_id}/assign-student")
async def assign_student_to_parent(
    parent_id: int,
    assignment_data: dict,
    db: AsyncSession = Depends(get_db),
    school_id: int = Depends(get_tenant_school_id),
):
    # Verify parent and student exist
    parent = await db.get(Parent, parent_id)
    if not parent or parent.school_id != school_id:
        raise HTTPException(status_code=404, detail="Parent not found")
    
    student = await db.get(Student, assignment_data["student_id"])
    if not student or student.school_id != school_id:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Create relationship
    relationship = ParentStudent(
        school_id=school_id,
        parent_id=parent_id,
        student_id=assignment_data["student_id"],
        relationship_type=assignment_data.get("relationship_type", "parent"),
        is_primary=assignment_data.get("is_primary", False)
    )
    db.add(relationship)
    await db.commit()
    return {"message": "Student assigned to parent successfully"} 