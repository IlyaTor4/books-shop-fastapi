from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response


SECURE_TOKEN = 'secure_token'


class TokenValidationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        token = request.headers.get("Authorization")

        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization header missing")

        if token != SECURE_TOKEN:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token")

        response = await call_next(request)
        return response
