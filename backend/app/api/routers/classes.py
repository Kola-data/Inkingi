from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ...api.deps import get_db, get_tenant_school_id
from ...models.academics import Class, ClassTeacher
from ...models.school import Staff
from ...schemas.classes import ClassCreate, ClassOut, AssignTeacherIn

router = APIRouter()


@router.post("", response_model=ClassOut)
async def create_class(
    payload: ClassCreate,
    db: AsyncSession = Depends(get_db),
    school_id: int = Depends(get_tenant_school_id),
):
    cls = Class(school_id=school_id, name=payload.name, level=payload.level, status="active")
    db.add(cls)
    await db.commit()
    await db.refresh(cls)
    return cls


@router.post("/{class_id}/assign-teacher")
async def assign_teacher(
    class_id: int,
    payload: AssignTeacherIn,
    db: AsyncSession = Depends(get_db),
    school_id: int = Depends(get_tenant_school_id),
):
    cls = await db.get(Class, class_id)
    if not cls or cls.school_id != school_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Class not found")
    teacher = await db.get(Staff, payload.staff_id)
    if not teacher or teacher.school_id != school_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Staff not found")
    assignment = ClassTeacher(school_id=school_id, class_id=class_id, staff_id=payload.staff_id)
    db.add(assignment)
    await db.commit()
    return {"ok": True} 