from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from ...api.deps import get_db, get_tenant_school_id
from ...models.academics import Course, CourseTeacher
from ...models.school import Staff

router = APIRouter()


@router.post("")
async def create_course(
    course_data: dict,
    db: AsyncSession = Depends(get_db),
    school_id: int = Depends(get_tenant_school_id),
):
    course = Course(
        school_id=school_id,
        code=course_data["code"],
        name=course_data["name"],
        description=course_data.get("description"),
        credit_hours=course_data.get("credit_hours"),
        status="active"
    )
    db.add(course)
    await db.commit()
    await db.refresh(course)
    return course


@router.get("")
async def list_courses(
    db: AsyncSession = Depends(get_db),
    school_id: int = Depends(get_tenant_school_id),
):
    result = await db.execute(
        select(Course).where(Course.school_id == school_id, Course.status == "active")
    )
    return result.scalars().all()


@router.post("/{course_id}/assign-teacher")
async def assign_teacher_to_course(
    course_id: int,
    assignment_data: dict,
    db: AsyncSession = Depends(get_db),
    school_id: int = Depends(get_tenant_school_id),
):
    # Verify course exists
    course = await db.get(Course, course_id)
    if not course or course.school_id != school_id:
        raise HTTPException(status_code=404, detail="Course not found")
    
    # Verify staff exists
    staff = await db.get(Staff, assignment_data["staff_id"])
    if not staff or staff.school_id != school_id:
        raise HTTPException(status_code=404, detail="Staff not found")
    
    # Create assignment
    assignment = CourseTeacher(
        school_id=school_id,
        course_id=course_id,
        staff_id=assignment_data["staff_id"]
    )
    db.add(assignment)
    await db.commit()
    return {"message": "Teacher assigned to course successfully"} 