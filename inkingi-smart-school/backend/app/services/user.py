"""
User service
"""
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.core.security import verify_password, get_password_hash
from app.models.user import User
from app.schemas.auth import UserCreate, UserUpdate


class UserService:
    """User service class"""
    
    def get_user(self, db: Session, user_id: int) -> Optional[User]:
        """Get user by ID"""
        return db.query(User).filter(User.id == user_id).first()
    
    def get_user_by_id(self, db: Session, user_id: int) -> Optional[User]:
        """Get user by ID with relationships"""
        return db.query(User).filter(User.id == user_id).first()
    
    def get_user_by_email(self, db: Session, email: str, school_id: Optional[int] = None) -> Optional[User]:
        """Get user by email"""
        query = db.query(User).filter(User.email == email)
        if school_id:
            query = query.filter(User.school_id == school_id)
        return query.first()
    
    def get_users(self, db: Session, school_id: int, skip: int = 0, limit: int = 100):
        """Get users for a school"""
        return db.query(User).filter(User.school_id == school_id).offset(skip).limit(limit).all()
    
    def create_user(self, db: Session, user_in: UserCreate) -> User:
        """Create new user"""
        hashed_password = get_password_hash(user_in.password)
        
        db_user = User(
            email=user_in.email,
            phone=user_in.phone,
            password_hash=hashed_password,
            school_id=user_in.school_id,
            staff_id=user_in.staff_id,
            status="pending"
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    def update_user(self, db: Session, user: User, user_in: UserUpdate) -> User:
        """Update user"""
        update_data = user_in.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(user, field, value)
        
        db.commit()
        db.refresh(user)
        return user
    
    def authenticate_user(self, db: Session, email: str, password: str) -> Optional[User]:
        """Authenticate user with email and password"""
        user = self.get_user_by_email(db, email)
        if not user:
            return None
        if not verify_password(password, user.password_hash):
            return None
        return user
    
    def activate_user(self, db: Session, user: User) -> User:
        """Activate user account"""
        user.status = "active"
        db.commit()
        db.refresh(user)
        return user
    
    def deactivate_user(self, db: Session, user: User) -> User:
        """Deactivate user account"""
        user.status = "inactive"
        db.commit()
        db.refresh(user)
        return user