from pydantic import BaseModel
from datetime import date


class AcademicYearCreate(BaseModel):
    name: str
    start_date: date | None = None
    end_date: date | None = None


class AcademicYearOut(BaseModel):
    id: int
    name: str
    is_current: bool

    class Config:
        from_attributes = True 