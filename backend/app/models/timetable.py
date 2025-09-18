from sqlalchemy import Column, String, Integer, ForeignKey, Time, Boolean, JSON
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class Period(BaseModel):
    __tablename__ = "periods"
    
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=False)
    name = Column(String(100), nullable=False)  # e.g., "Period 1", "Morning Assembly"
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    order_index = Column(Integer, nullable=False)
    is_break = Column(Boolean, default=False)
    status = Column(String(20), default="active")  # active, inactive
    
    # Relationships
    school = relationship("School")
    timetables = relationship("Timetable", back_populates="period")

class Room(BaseModel):
    __tablename__ = "rooms"
    
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=False)
    name = Column(String(100), nullable=False)  # e.g., "Room 101", "Library"
    code = Column(String(50), nullable=True)  # e.g., "R101"
    capacity = Column(Integer, nullable=True)
    room_type = Column(String(50), nullable=True)  # classroom, lab, library, hall
    location = Column(String(255), nullable=True)
    equipment = Column(JSON, nullable=True)  # List of available equipment
    status = Column(String(20), default="active")  # active, inactive, maintenance
    
    # Relationships
    school = relationship("School")
    timetables = relationship("Timetable", back_populates="room")

class Timetable(BaseModel):
    __tablename__ = "timetables"
    
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=False)
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=True)
    period_id = Column(Integer, ForeignKey("periods.id"), nullable=False)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=True)
    staff_id = Column(Integer, ForeignKey("staff.id"), nullable=True)
    day_of_week = Column(Integer, nullable=False)  # 0=Monday, 6=Sunday
    week_number = Column(Integer, nullable=True)  # For weekly timetables
    academic_year_id = Column(Integer, ForeignKey("academic_years.id"), nullable=True)
    term_id = Column(Integer, ForeignKey("terms.id"), nullable=True)
    status = Column(String(20), default="active")  # active, inactive, cancelled
    
    # Relationships
    school = relationship("School")
    class_entity = relationship("Class")
    course = relationship("Course")
    period = relationship("Period", back_populates="timetables")
    room = relationship("Room", back_populates="timetables")
    staff = relationship("Staff")
    academic_year = relationship("AcademicYear")
    term = relationship("Term")