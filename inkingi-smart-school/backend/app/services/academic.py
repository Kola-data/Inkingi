"""
Academic services for classes, enrollment, etc.
"""
from typing import Optional, List
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.models.academic import AcademicYear, Term, Class, ClassTeacher, Enrollment
from app.models.staff import Staff
from app.schemas.academic import (
    AcademicYearCreate, TermCreate, ClassCreate, ClassUpdate, EnrollmentCreate
)


class AcademicYearService:
    """Academic year service"""
    
    def get_academic_year(self, db: Session, year_id: int, school_id: int) -> Optional[AcademicYear]:
        """Get academic year by ID"""
        return db.query(AcademicYear).filter(
            and_(AcademicYear.id == year_id, AcademicYear.school_id == school_id)
        ).first()
    
    def get_current_academic_year(self, db: Session, school_id: int) -> Optional[AcademicYear]:
        """Get current academic year for school"""
        return db.query(AcademicYear).filter(
            and_(AcademicYear.school_id == school_id, AcademicYear.is_current == True)
        ).first()
    
    def get_academic_years(self, db: Session, school_id: int, skip: int = 0, limit: int = 100) -> List[AcademicYear]:
        """Get academic years for school"""
        return db.query(AcademicYear).filter(
            AcademicYear.school_id == school_id
        ).offset(skip).limit(limit).all()
    
    def create_academic_year(self, db: Session, year_in: AcademicYearCreate, school_id: int) -> AcademicYear:
        """Create new academic year"""
        # If this is set as current, unset other current years
        if year_in.is_current:
            db.query(AcademicYear).filter(
                and_(AcademicYear.school_id == school_id, AcademicYear.is_current == True)
            ).update({"is_current": False})
        
        db_year = AcademicYear(
            school_id=school_id,
            name=year_in.name,
            start_date=year_in.start_date,
            end_date=year_in.end_date,
            is_current=year_in.is_current
        )
        
        db.add(db_year)
        db.commit()
        db.refresh(db_year)
        return db_year


class ClassService:
    """Class service"""
    
    def get_class(self, db: Session, class_id: int, school_id: int) -> Optional[Class]:
        """Get class by ID"""
        return db.query(Class).filter(
            and_(Class.id == class_id, Class.school_id == school_id)
        ).first()
    
    def get_class_by_name(self, db: Session, school_id: int, name: str) -> Optional[Class]:
        """Get class by name"""
        return db.query(Class).filter(
            and_(Class.school_id == school_id, Class.name == name)
        ).first()
    
    def get_classes(self, db: Session, school_id: int, skip: int = 0, limit: int = 100) -> List[Class]:
        """Get classes for school"""
        return db.query(Class).filter(
            Class.school_id == school_id
        ).offset(skip).limit(limit).all()
    
    def create_class(self, db: Session, class_in: ClassCreate, school_id: int) -> Class:
        """Create new class"""
        db_class = Class(
            school_id=school_id,
            name=class_in.name,
            level=class_in.level,
            status="active"
        )
        
        db.add(db_class)
        db.commit()
        db.refresh(db_class)
        return db_class
    
    def update_class(self, db: Session, class_obj: Class, class_in: ClassUpdate) -> Class:
        """Update class"""
        update_data = class_in.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(class_obj, field, value)
        
        db.commit()
        db.refresh(class_obj)
        return class_obj
    
    def delete_class(self, db: Session, class_obj: Class) -> None:
        """Delete class"""
        db.delete(class_obj)
        db.commit()
    
    def assign_teacher_to_class(self, db: Session, class_id: int, staff_id: int, school_id: int) -> ClassTeacher:
        """Assign teacher to class"""
        # Verify staff exists and belongs to school
        staff = db.query(Staff).filter(
            and_(Staff.id == staff_id, Staff.school_id == school_id)
        ).first()
        
        if not staff:
            raise ValueError("Staff member not found")
        
        # Check if there's already an active assignment
        existing = db.query(ClassTeacher).filter(
            and_(
                ClassTeacher.class_id == class_id,
                ClassTeacher.school_id == school_id
            )
        ).first()
        
        if existing:
            # Update existing assignment
            existing.staff_id = staff_id
            existing.assigned_at = datetime.utcnow()
            db.commit()
            db.refresh(existing)
            return existing
        else:
            # Create new assignment
            assignment = ClassTeacher(
                school_id=school_id,
                class_id=class_id,
                staff_id=staff_id,
                assigned_at=datetime.utcnow()
            )
            
            db.add(assignment)
            db.commit()
            db.refresh(assignment)
            return assignment


class EnrollmentService:
    """Enrollment service"""
    
    def get_enrollment(self, db: Session, enrollment_id: int, school_id: int) -> Optional[Enrollment]:
        """Get enrollment by ID"""
        return db.query(Enrollment).filter(
            and_(Enrollment.id == enrollment_id, Enrollment.school_id == school_id)
        ).first()
    
    def get_enrollment_by_student_class_year(
        self, 
        db: Session, 
        student_id: int, 
        class_id: int, 
        academic_year_id: int,
        school_id: int
    ) -> Optional[Enrollment]:
        """Get enrollment by student, class, and academic year"""
        return db.query(Enrollment).filter(
            and_(
                Enrollment.student_id == student_id,
                Enrollment.class_id == class_id,
                Enrollment.academic_year_id == academic_year_id,
                Enrollment.school_id == school_id,
                Enrollment.status == "active"
            )
        ).first()
    
    def get_enrollments(
        self, 
        db: Session, 
        school_id: int,
        skip: int = 0, 
        limit: int = 100,
        class_id: Optional[int] = None,
        student_id: Optional[int] = None,
        academic_year_id: Optional[int] = None
    ) -> List[Enrollment]:
        """Get enrollments with optional filters"""
        query = db.query(Enrollment).filter(Enrollment.school_id == school_id)
        
        if class_id:
            query = query.filter(Enrollment.class_id == class_id)
        if student_id:
            query = query.filter(Enrollment.student_id == student_id)
        if academic_year_id:
            query = query.filter(Enrollment.academic_year_id == academic_year_id)
        
        return query.offset(skip).limit(limit).all()
    
    def create_enrollment(self, db: Session, enrollment_in: EnrollmentCreate, school_id: int) -> Enrollment:
        """Create new enrollment"""
        db_enrollment = Enrollment(
            school_id=school_id,
            student_id=enrollment_in.student_id,
            class_id=enrollment_in.class_id,
            academic_year_id=enrollment_in.academic_year_id,
            enrolled_at=datetime.utcnow(),
            status="active"
        )
        
        db.add(db_enrollment)
        db.commit()
        db.refresh(db_enrollment)
        return db_enrollment
    
    def withdraw_enrollment(self, db: Session, enrollment: Enrollment) -> Enrollment:
        """Withdraw enrollment (change status)"""
        enrollment.status = "withdrawn"
        db.commit()
        db.refresh(enrollment)
        return enrollment