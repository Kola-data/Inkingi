from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
import re


class TenantMiddleware(BaseHTTPMiddleware):
    """Extract and validate tenant from subdomain or header"""
    
    async def dispatch(self, request: Request, call_next):
        # Skip tenant check for certain paths
        skip_paths = ["/", "/health", "/metrics", "/api/v1/auth/login", "/api/v1/auth/register"]
        if any(request.url.path.startswith(path) for path in skip_paths):
            return await call_next(request)
        
        # Try to extract tenant from subdomain
        host = request.headers.get("host", "")
        tenant_slug = None
        
        # Check subdomain (e.g., school1.app.com)
        if "." in host:
            subdomain = host.split(".")[0]
            if subdomain and subdomain not in ["www", "api", "app"]:
                tenant_slug = subdomain
        
        # Check X-Tenant-ID header (for API clients)
        if not tenant_slug:
            tenant_slug = request.headers.get("x-tenant-id")
        
        # Store in request state for later use
        request.state.tenant_slug = tenant_slug
        
        # For now, we'll allow requests without tenant for development
        # In production, you'd want to enforce this for tenant-specific endpoints
        
        response = await call_next(request)
        return response