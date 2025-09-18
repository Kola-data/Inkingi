"""
Tenant service for multi-tenancy
"""
from typing import Optional
from sqlalchemy.orm import Session

from app.models.school import School


class TenantService:
    """Tenant service for resolving tenant context"""
    
    async def get_tenant_id_by_slug(self, db: Session, slug: str) -> Optional[int]:
        """Get tenant ID by school slug"""
        school = db.query(School).filter(School.slug == slug).first()
        return school.id if school else None
    
    async def get_tenant_id_by_domain(self, db: Session, domain: str) -> Optional[int]:
        """Get tenant ID by custom domain (future implementation)"""
        # TODO: Implement custom domain mapping table
        # For now, return None - only subdomain routing is supported
        return None
    
    def get_school_by_tenant_id(self, db: Session, tenant_id: int) -> Optional[School]:
        """Get school by tenant ID"""
        return db.query(School).filter(School.id == tenant_id).first()