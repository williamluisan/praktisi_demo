from pydantic import BaseModel

class Login(BaseModel):
    username: str
    password: str

class AuthRefreshToken(BaseModel):
    refresh_token: str