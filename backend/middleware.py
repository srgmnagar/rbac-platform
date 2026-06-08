from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from .config import config

class APIKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Allow health check and docs without API key
        if request.url.path in ["/health", "/docs", "/openapi.json", "/redoc"]:
            return await call_next(request)
        
        # Check API key
        api_key = request.headers.get("X-API-Key")
        if api_key != config.API_KEY:
            raise HTTPException(status_code=401, detail="Invalid API key")
        
        return await call_next(request)
