#!/usr/bin/env python3
"""
Seed database with initial data
"""
import os
import sys
from datetime import datetime, date

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.db.session import SessionLocal, engine
from app.models import *
from app.core.security import get_password_hash

def seed_data():
    """Seed database with initial data"""
    db = SessionLocal()
    
    try:
        # Create roles
        roles_data = [
            {"name": "system_admin", "scope": "system", "description": "System administrator with full access"},
            {"name": "school_admin", "scope": "school", "description": "School administrator"},
            {"name": "accountant", "scope": "school", "description": "School accountant"},
            {"name": "teacher", "scope": "school", "description": "Teacher"},
            {"name": "parent", "scope": "school", "description": "Parent with limited access"},
        ]
        
        for role_data in roles_data:
            role = db.query(Role).filter(Role.name == role_data["name"]).first()
            if not role:
                role = Role(**role_data)
                db.add(role)
        
        # Create permissions
        permissions_data = [
            {"name": "school:create", "resource": "school", "action": "create"},
            {"name": "school:read", "resource": "school", "action": "read"},
            {"name": "school:update", "resource": "school", "action": "update"},
            {"name": "school:delete", "resource": "school", "action": "delete"},
            
            {"name": "class:create", "resource": "class", "action": "create"},
            {"name": "class:read", "resource": "class", "action": "read"},
            {"name": "class:update", "resource": "class", "action": "update"},
            {"name": "class:delete", "resource": "class", "action": "delete"},
            
            {"name": "enrollment:create", "resource": "enrollment", "action": "create"},
            {"name": "enrollment:read", "resource": "enrollment", "action": "read"},
            {"name": "enrollment:update", "resource": "enrollment", "action": "update"},
            {"name": "enrollment:delete", "resource": "enrollment", "action": "delete"},
            
            {"name": "user:create", "resource": "user", "action": "create"},
            {"name": "user:read", "resource": "user", "action": "read"},
            {"name": "user:update", "resource": "user", "action": "update"},
            {"name": "user:delete", "resource": "user", "action": "delete"},
        ]
        
        for perm_data in permissions_data:
            permission = db.query(Permission).filter(Permission.name == perm_data["name"]).first()
            if not permission:
                permission = Permission(**perm_data)
                db.add(permission)
        
        db.commit()
        
        # Create demo school
        demo_school = db.query(School).filter(School.slug == "demo").first()
        if not demo_school:
            demo_school = School(
                name="Demo School",
                slug="demo",
                status="active",
                contact_email="admin@demo.school",
                contact_phone="+1234567890",
                address_json={
                    "street": "123 Education Ave",
                    "city": "Learning City",
                    "state": "Knowledge State",
                    "zip": "12345",
                    "country": "Education Land"
                },
                verified_at=datetime.utcnow()
            )
            db.add(demo_school)
            db.commit()
        
        # Create demo academic year
        current_year = db.query(AcademicYear).filter(
            AcademicYear.school_id == demo_school.id,
            AcademicYear.is_current == True
        ).first()
        
        if not current_year:
            current_year = AcademicYear(
                school_id=demo_school.id,
                name="2024/2025",
                start_date=date(2024, 9, 1),
                end_date=date(2025, 8, 31),
                is_current=True
            )
            db.add(current_year)
            db.commit()
        
        # Create demo staff
        demo_staff = db.query(Staff).filter(
            Staff.school_id == demo_school.id,
            Staff.email == "admin@demo.school"
        ).first()
        
        if not demo_staff:
            demo_staff = Staff(
                school_id=demo_school.id,
                first_name="Demo",
                last_name="Admin",
                email="admin@demo.school",
                phone="+1234567890",
                position="Principal",
                department="Administration",
                hire_date=date(2024, 1, 1),
                status="active"
            )
            db.add(demo_staff)
            db.commit()
        
        # Create demo admin user
        admin_user = db.query(User).filter(User.email == "admin@demo.school").first()
        if not admin_user:
            admin_user = User(
                school_id=demo_school.id,
                staff_id=demo_staff.id,
                email="admin@demo.school",
                password_hash=get_password_hash("admin123"),
                status="active"
            )
            db.add(admin_user)
            db.commit()
            
            # Assign school_admin role
            school_admin_role = db.query(Role).filter(Role.name == "school_admin").first()
            if school_admin_role:
                admin_user.roles.append(school_admin_role)
                db.commit()
        
        # Create demo classes
        demo_classes = [
            {"name": "P1", "level": "Primary"},
            {"name": "P2", "level": "Primary"},
            {"name": "P3", "level": "Primary"},
            {"name": "S1", "level": "Secondary"},
            {"name": "S2", "level": "Secondary"},
        ]
        
        for class_data in demo_classes:
            existing_class = db.query(Class).filter(
                Class.school_id == demo_school.id,
                Class.name == class_data["name"]
            ).first()
            
            if not existing_class:
                demo_class = Class(
                    school_id=demo_school.id,
                    name=class_data["name"],
                    level=class_data["level"],
                    status="active"
                )
                db.add(demo_class)
        
        db.commit()
        print("✅ Database seeded successfully!")
        
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()