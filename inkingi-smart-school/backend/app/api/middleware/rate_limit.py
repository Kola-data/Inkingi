from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
import time
import redis.asyncio as redis
from app.core.config import settings


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Rate limiting middleware using Redis"""
    
    def __init__(self, app):
        super().__init__(app)
        self.redis_client = None
        
    async def dispatch(self, request: Request, call_next):
        # Skip rate limiting for certain paths
        skip_paths = ["/health", "/metrics"]
        if any(request.url.path.startswith(path) for path in skip_paths):
            return await call_next(request)
        
        # Initialize Redis client if not already done
        if not self.redis_client:
            try:
                self.redis_client = await redis.from_url(settings.REDIS_URL)
            except Exception:
                # If Redis is not available, skip rate limiting
                return await call_next(request)
        
        # Get client identifier (IP address or user ID)
        client_id = request.client.host if request.client else "unknown"
        
        # Create rate limit key
        key = f"rate_limit:{client_id}:{int(time.time() // settings.RATE_LIMIT_PERIOD)}"
        
        try:
            # Check and increment counter
            current = await self.redis_client.incr(key)
            
            # Set expiry on first request
            if current == 1:
                await self.redis_client.expire(key, settings.RATE_LIMIT_PERIOD)
            
            # Check if limit exceeded
            if current > settings.RATE_LIMIT_REQUESTS:
                return JSONResponse(
                    status_code=429,
                    content={"detail": "Rate limit exceeded. Please try again later."},
                    headers={
                        "X-RateLimit-Limit": str(settings.RATE_LIMIT_REQUESTS),
                        "X-RateLimit-Remaining": "0",
                        "X-RateLimit-Reset": str(int(time.time()) + settings.RATE_LIMIT_PERIOD),
                    },
                )
            
            # Process request
            response = await call_next(request)
            
            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(settings.RATE_LIMIT_REQUESTS)
            response.headers["X-RateLimit-Remaining"] = str(settings.RATE_LIMIT_REQUESTS - current)
            response.headers["X-RateLimit-Reset"] = str(int(time.time()) + settings.RATE_LIMIT_PERIOD)
            
            return response
            
        except Exception:
            # If Redis fails, allow the request
            return await call_next(request)