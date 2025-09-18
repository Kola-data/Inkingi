"""
Custom middleware for the application
"""
import re
from typing import Optional
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from app.core.security import decode_access_token
from app.db.session import get_db
from app.services.tenant import TenantService


class TenantMiddleware(BaseHTTPMiddleware):
    """
    Middleware to handle multi-tenancy by extracting tenant information
    from subdomain or custom domain and setting it in the database context
    """
    
    def __init__(self, app):
        super().__init__(app)
        self.tenant_service = TenantService()
    
    async def dispatch(self, request: Request, call_next):
        # Skip tenant resolution for health check and docs endpoints
        if request.url.path in ["/health", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)
        
        try:
            tenant_id = await self._resolve_tenant(request)
            if tenant_id:
                request.state.tenant_id = tenant_id
            
            response = await call_next(request)
            return response
            
        except HTTPException as e:
            return Response(
                content=f'{{"detail": "{e.detail}"}}',
                status_code=e.status_code,
                media_type="application/json"
            )
        except Exception as e:
            return Response(
                content=f'{{"detail": "Internal server error"}}',
                status_code=500,
                media_type="application/json"
            )
    
    async def _resolve_tenant(self, request: Request) -> Optional[int]:
        """
        Resolve tenant ID from request
        Priority: JWT token claims > subdomain > custom domain
        """
        
        # Try to get tenant from JWT token first
        tenant_id = await self._get_tenant_from_token(request)
        if tenant_id:
            return tenant_id
        
        # Try to get tenant from domain/subdomain
        tenant_id = await self._get_tenant_from_domain(request)
        if tenant_id:
            return tenant_id
        
        # For development, allow requests without tenant (will be handled by endpoints)
        return None
    
    async def _get_tenant_from_token(self, request: Request) -> Optional[int]:
        """Extract tenant ID from JWT token"""
        try:
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                return None
            
            token = auth_header.split(" ")[1]
            payload = decode_access_token(token)
            return payload.get("tenant_id")
            
        except Exception:
            return None
    
    async def _get_tenant_from_domain(self, request: Request) -> Optional[int]:
        """Extract tenant ID from domain/subdomain"""
        try:
            host = request.headers.get("host", "")
            
            # Extract subdomain pattern: {school_slug}.app.com
            subdomain_match = re.match(r"^([^.]+)\.app\.com$", host)
            if subdomain_match:
                school_slug = subdomain_match.group(1)
                async with get_db() as db:
                    return await self.tenant_service.get_tenant_id_by_slug(db, school_slug)
            
            # Check for custom domain mapping
            async with get_db() as db:
                return await self.tenant_service.get_tenant_id_by_domain(db, host)
                
        except Exception:
            return None