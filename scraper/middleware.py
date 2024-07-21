from fastapi import Request, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from scraper.constants import STATIC_AUTH_TOKEN


# Middleware to check for the static token
class TokenAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        auth_header = request.headers.get("Authorization")
        if auth_header is None or auth_header != STATIC_AUTH_TOKEN:
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={"detail": "Invalid authentication credentials"},
            )
        return await call_next(request)
