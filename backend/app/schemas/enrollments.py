from pydantic import BaseModel


class EnrollmentCreate(BaseModel):
    student_id: int
    class_id: int
    academic_year_id: int | None = None


class EnrollmentOut(BaseModel):
    id: int
    student_id: int
    class_id: int
    academic_year_id: int
    status: str

    class Config:
        from_attributes = True 