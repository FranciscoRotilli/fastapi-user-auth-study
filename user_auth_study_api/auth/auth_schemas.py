from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    """
    Token response schema, sent to user on login.
    """
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """
    JWT token content schema.
    """
    username: Optional[str] = None
    role: str | None = None