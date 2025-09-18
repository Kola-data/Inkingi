from pydantic import BaseModel
from typing import Optional
from datetime import time

class PeriodBase(BaseModel):
    name: str
    start_time: time
    end_time: time
    order_index: int
    is_break: bool = False

class PeriodCreate(PeriodBase):
    pass

class PeriodUpdate(BaseModel):
    name: Optional[str] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    order_index: Optional[int] = None
    is_break: Optional[bool] = None
    status: Optional[str] = None

class PeriodResponse(PeriodBase):
    id: int
    school_id: int
    status: str
    created_at: str
    updated_at: Optional[str]
    
    class Config:
        from_attributes = True

class RoomBase(BaseModel):
    name: str
    code: Optional[str] = None
    capacity: Optional[int] = None
    room_type: Optional[str] = None
    location: Optional[str] = None

class RoomCreate(RoomBase):
    pass

class RoomUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    capacity: Optional[int] = None
    room_type: Optional[str] = None
    location: Optional[str] = None
    status: Optional[str] = None

class RoomResponse(RoomBase):
    id: int
    school_id: int
    status: str
    created_at: str
    updated_at: Optional[str]
    
    class Config:
        from_attributes = True

class TimetableBase(BaseModel):
    class_id: Optional[int] = None
    course_id: Optional[int] = None
    period_id: int
    room_id: Optional[int] = None
    staff_id: Optional[int] = None
    day_of_week: int
    week_number: Optional[int] = None
    academic_year_id: Optional[int] = None
    term_id: Optional[int] = None

class TimetableCreate(TimetableBase):
    pass

class TimetableUpdate(BaseModel):
    class_id: Optional[int] = None
    course_id: Optional[int] = None
    period_id: Optional[int] = None
    room_id: Optional[int] = None
    staff_id: Optional[int] = None
    day_of_week: Optional[int] = None
    week_number: Optional[int] = None
    academic_year_id: Optional[int] = None
    term_id: Optional[int] = None
    status: Optional[str] = None

class TimetableResponse(TimetableBase):
    id: int
    school_id: int
    status: str
    created_at: str
    updated_at: Optional[str]
    
    class Config:
        from_attributes = True