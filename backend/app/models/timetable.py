from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Time, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..db.session import Base


class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    code = Column(String(50), nullable=True)
    capacity = Column(Integer, nullable=True)
    room_type = Column(String(50), nullable=True)  # classroom, lab, library, etc.
    location = Column(String(255), nullable=True)
    equipment = Column(Text, nullable=True)  # JSON string of equipment
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Period(Base):
    __tablename__ = "periods"

    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, nullable=False, index=True)
    name = Column(String(100), nullable=False)  # Period 1, Period 2, etc.
    weekday = Column(Integer, nullable=False)  # 0=Monday, 6=Sunday
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    period_type = Column(String(50), nullable=True)  # regular, break, lunch
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Timetable(Base):
    __tablename__ = "timetables"

    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, nullable=False, index=True)
    class_id = Column(Integer, ForeignKey('classes.id'), nullable=False, index=True)
    term_id = Column(Integer, ForeignKey('terms.id'), nullable=False, index=True)
    academic_year_id = Column(Integer, ForeignKey('academic_years.id'), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(50), nullable=False, default="draft")  # draft, active, archived
    effective_date = Column(DateTime(timezone=True), nullable=True)
    created_by = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    class_ = relationship("Class", back_populates="timetables")
    term = relationship("Term")
    academic_year = relationship("AcademicYear")
    entries = relationship("TimetableEntry", back_populates="timetable", cascade="all, delete-orphan")
    creator = relationship("User")


class TimetableEntry(Base):
    __tablename__ = "timetable_entries"

    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, nullable=False, index=True)
    timetable_id = Column(Integer, ForeignKey('timetables.id'), nullable=False, index=True)
    period_id = Column(Integer, ForeignKey('periods.id'), nullable=False, index=True)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False, index=True)
    staff_id = Column(Integer, ForeignKey('staff.id'), nullable=False, index=True)
    room_id = Column(Integer, ForeignKey('rooms.id'), nullable=True, index=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    timetable = relationship("Timetable", back_populates="entries")
    period = relationship("Period")
    course = relationship("Course")
    staff = relationship("Staff")
    room = relationship("Room")


class TeacherAvailability(Base):
    __tablename__ = "teacher_availability"

    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, nullable=False, index=True)
    staff_id = Column(Integer, ForeignKey('staff.id'), nullable=False, index=True)
    weekday = Column(Integer, nullable=False)  # 0=Monday, 6=Sunday
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    availability_type = Column(String(50), nullable=False, default="available")  # available, unavailable
    reason = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    staff = relationship("Staff") 