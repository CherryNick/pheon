from pydantic import BaseModel, Field


class TokenResponse(BaseModel):
    access_token: str = Field(..., examples=["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"])
    refresh_token: str = Field(..., examples=["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"])
    token_type: str = Field("bearer", examples=["bearer"])


class LogoutResponse(BaseModel):
    message: str = Field("Successfully logged out")
