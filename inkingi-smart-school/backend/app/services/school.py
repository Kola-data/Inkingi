"""
School service
"""
from typing import Optional, List
from sqlalchemy.orm import Session

from app.models.school import School
from app.schemas.school import SchoolCreate, SchoolUpdate


class SchoolService:
    """School service class"""
    
    def get_school(self, db: Session, school_id: int) -> Optional[School]:
        """Get school by ID"""
        return db.query(School).filter(School.id == school_id).first()
    
    def get_school_by_slug(self, db: Session, slug: str) -> Optional[School]:
        """Get school by slug"""
        return db.query(School).filter(School.slug == slug).first()
    
    def get_schools(self, db: Session, skip: int = 0, limit: int = 100) -> List[School]:
        """Get all schools"""
        return db.query(School).offset(skip).limit(limit).all()
    
    def create_school(self, db: Session, school_in: SchoolCreate) -> School:
        """Create new school"""
        db_school = School(
            name=school_in.name,
            slug=school_in.slug,
            contact_email=school_in.contact_email,
            contact_phone=school_in.contact_phone,
            address_json=school_in.address_json,
            status="pending"
        )
        
        db.add(db_school)
        db.commit()
        db.refresh(db_school)
        return db_school
    
    def update_school(self, db: Session, school: School, school_in: SchoolUpdate) -> School:
        """Update school"""
        update_data = school_in.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(school, field, value)
        
        db.commit()
        db.refresh(school)
        return school
    
    def verify_school(self, db: Session, school: School) -> School:
        """Verify school"""
        from datetime import datetime
        school.status = "active"
        school.verified_at = datetime.utcnow()
        db.commit()
        db.refresh(school)
        return school
    
    def suspend_school(self, db: Session, school: School) -> School:
        """Suspend school"""
        school.status = "suspended"
        db.commit()
        db.refresh(school)
        return school