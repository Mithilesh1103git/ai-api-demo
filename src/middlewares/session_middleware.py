from fastapi import status
from fastapi.requests import Request
from fastapi.exceptions import HTTPException
from starlette.middleware.base import BaseHTTPMiddleware

class CustomSessionCheckerMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        # print(f"request session: {request.session}")
        
        if request.user.is_authenticated:
            if "session_id" not in request.session.keys():
                request.session["session_id"] = "my-test-session-id"
                request.state.session_alive = True
                print("Session ID not found, adding one now.")
            else:
                print("Session ID found.")
                print(f"request session id: {request.session.get("session-id")}")
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User not authenticated. Session can not be granted.")

        return await call_next(request)
