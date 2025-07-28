from fastapi.requests import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.authentication import AuthCredentials, BaseUser, AuthenticationBackend

class CustomUser(BaseUser):
    def __init__(self, username: str, role: str):
        self.user_name = username
        self.role = role

    @property
    def display_name(self) -> str:
        return self.user_name

    @property
    def identity(self) -> str:
        return self.role
    
    @property
    def is_authenticated(self) -> bool:
        return True

class CustomAuthenticationBackend(AuthenticationBackend):
    async def authenticate(self, conn):
        # print(conn)

        if 'authorization' in conn.headers.keys():
            print("Auth header found.")
            auth_creds = AuthCredentials(["authenticated", "user"])
            user_details = CustomUser(username="Mithilesh", role="SuperAdmin")
            return auth_creds, user_details
        
        return None

