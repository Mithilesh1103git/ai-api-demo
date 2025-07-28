from fastapi.requests import Request
from starlette.middleware.base import BaseHTTPMiddleware


class CustomRequestInterceptorMw(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # request_body = await request.body()
        # print(request_body)

        if 'authorization' in request.headers.keys():
            request.state.user = {"username": "alice", "role": "admin", "is_authenticated": True}

        # request_elements = request.items()
        # print([e for e in request_elements])
        # print(vars(request.state))
        
        return await call_next(request)
