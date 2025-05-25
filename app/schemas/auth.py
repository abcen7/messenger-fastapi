from datetime import datetime
from typing import Literal

from pydantic import BaseModel, EmailStr

from app.utils.constants import ACCESS_TOKEN_TYPE, BEARER_TOKEN_TYPE, REFRESH_TOKEN_TYPE


class TokenPayload(BaseModel):
    sub: str  # user_id
    iat: datetime  # issued at
    exp: datetime  # expires at
    type: Literal["access", "refresh"]


class AccessTokenPayload(TokenPayload):
    type: Literal["access"] = ACCESS_TOKEN_TYPE


class RefreshTokenPayload(TokenPayload):
    type: Literal["refresh"] = REFRESH_TOKEN_TYPE


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: Literal["Bearer"] = BEARER_TOKEN_TYPE
