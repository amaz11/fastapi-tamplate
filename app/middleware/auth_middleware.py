from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request


class DemoHeaderMiddleware(BaseHTTPMiddleware):
    """
    Add header so beginner can see middleware effect.
    Middleware runs before response leaves app.
    """

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["X-App-Mode"] = "learning"
        return response
