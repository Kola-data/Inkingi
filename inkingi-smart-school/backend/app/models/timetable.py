from sqlalchemy import Column, String, Time, ForeignKey, Integer, Enum as SQLEnum, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import TenantModel
import enum


class DayOfWeek(str, enum.Enum):
    MONDAY = "monday"
    TUESDAY = "tuesday"
    WEDNESDAY = "wednesday"
    THURSDAY = "thursday"
    FRIDAY = "friday"
    SATURDAY = "saturday"
    SUNDAY = "sunday"


class Period(TenantModel):
    __tablename__ = "periods"
    __table_args__ = (
        UniqueConstraint("school_id", "name", name="uq_period_name"),
    )
    
    name = Column(String(50), nullable=False)  # e.g., "Period 1", "Break"
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    order_index = Column(Integer, nullable=False)
    is_break = Column(String, default="false", nullable=False)
    
    # Relationships
    timetable_entries = relationship("TimetableEntry", back_populates="period")
    
    def __repr__(self):
        return f"<Period {self.name}>"


class Room(TenantModel):
    __tablename__ = "rooms"
    __table_args__ = (
        UniqueConstraint("school_id", "name", name="uq_room_name"),
    )
    
    name = Column(String(50), nullable=False)  # e.g., "Lab 1", "Class 3A"
    building = Column(String(50), nullable=True)
    floor = Column(String(10), nullable=True)
    capacity = Column(Integer, nullable=True)
    room_type = Column(String(50), nullable=True)  # e.g., "classroom", "lab", "hall"
    facilities = Column(String, nullable=True)  # JSON array of facilities
    
    # Relationships
    timetable_entries = relationship("TimetableEntry", back_populates="room")
    
    def __repr__(self):
        return f"<Room {self.name}>"


class TimetableEntry(TenantModel):
    __tablename__ = "timetable_entries"
    __table_args__ = (
        UniqueConstraint("school_id", "class_id", "day_of_week", "period_id", name="uq_timetable_slot"),
    )
    
    class_id = Column(UUID(as_uuid=True), ForeignKey("classes.id"), nullable=False)
    course_id = Column(UUID(as_uuid=True), ForeignKey("courses.id"), nullable=False)
    teacher_id = Column(UUID(as_uuid=True), ForeignKey("staff.id"), nullable=False)
    room_id = Column(UUID(as_uuid=True), ForeignKey("rooms.id"), nullable=True)
    period_id = Column(UUID(as_uuid=True), ForeignKey("periods.id"), nullable=False)
    day_of_week = Column(SQLEnum(DayOfWeek), nullable=False)
    
    # Relationships
    class_obj = relationship("Class", back_populates="timetable_entries")
    course = relationship("Course", back_populates="timetable_entries")
    period = relationship("Period", back_populates="timetable_entries")
    room = relationship("Room", back_populates="timetable_entries")
    
    def __repr__(self):
        return f"<TimetableEntry {self.class_id} - {self.course_id} on {self.day_of_week}>"