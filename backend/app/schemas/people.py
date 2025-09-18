from pydantic import BaseModel


class StaffCreate(BaseModel):
    first_name: str
    last_name: str
    email: str | None = None
    phone: str | None = None
    position: str | None = None


class StaffOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str | None = None
    phone: str | None = None
    position: str | None = None

    class Config:
        from_attributes = True


class StudentCreate(BaseModel):
    first_name: str
    last_name: str
    admission_no: str | None = None


class StudentOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    admission_no: str | None = None

    class Config:
        from_attributes = True 