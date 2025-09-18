from pydantic import BaseModel


class ClassCreate(BaseModel):
    name: str
    level: str | None = None


class ClassOut(BaseModel):
    id: int
    name: str
    level: str | None = None
    status: str

    class Config:
        from_attributes = True


class AssignTeacherIn(BaseModel):
    staff_id: int 