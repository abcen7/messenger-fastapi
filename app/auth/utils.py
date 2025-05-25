# TODO: make injections by classes
# class TokenBearer(HTTPBearer):
#     def __init__(self, auto_error=True):
#         super().__init__(auto_error=auto_error)
#
#     # TODO: Add return type
#     async def __call__(self, request: Request):
#         creds: HTTPAuthorizationCredentials = await super().__call__(request)
#         token: str = creds.credentials
#         token_data = AuthHelper.decode_access_token(token)
#
#         if not self.is_token_valid(token):
#             raise HTTPException(status_code=403, detail="Invalid token")
#
#         # TODO: blacklist Rate Limit Middleware
#         # if await token_in_blocklist(token_data["jti"]):
#         #     raise HTTPException(status_code=403, detail="Invalid token")
#
#         self.verify_token_data(token_data)
#
#         return token_data
#
#     @staticmethod
#     def is_token_valid(token: str) -> bool:
#         token_data = AuthHelper.decode_access_token(token)
#
#         return token_data is not None
#
#     def verify_token_data(self, token_data):
#         raise NotImplementedError("Please Override this method in child classes")
#
#
# class AccessTokenBearer(TokenBearer):
#     def verify_token_data(self, token_data: dict) -> None:
#         if token_data and token_data["refresh"]:
#             raise HTTPException(detail="Access token is invalid", status_code=403)
#
#
# class RefreshTokenBearer(TokenBearer):
#     def verify_token_data(self, token_data: dict) -> None:
#         if token_data and not token_data["refresh"]:
#             raise HTTPException(detail="Refresh token is invalid", status_code=403)


from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import HTTPException, Security
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
    OAuth2PasswordBearer,
)
from jwt import InvalidTokenError
from passlib.context import CryptContext
from pydantic import EmailStr
from starlette import status

from app.auth.schemas import AccessTokenPayload, RefreshTokenPayload, TokenPayload
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
bearer_scheme = HTTPBearer(bearerFormat="JWT")


class AuthHelper:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    @staticmethod
    def verify_password(plain_password, hashed_password) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password) -> str:
        return pwd_context.hash(password)

    # TODO: refactor
    @staticmethod
    def create_access_token(user_id: int):
        jwt_payload: AccessTokenPayload = (
            AccessTokenPayload(
                sub=str(user_id),
                iat=datetime.now(timezone.utc),
                exp=datetime.now(timezone.utc)
                + timedelta(minutes=settings.app.ACCESS_TOKEN_EXPIRE_MINUTES),
            )
            .model_dump()
            .copy()
        )
        encoded_jwt = jwt.encode(
            payload=jwt_payload,
            key=settings.app.SECRET_KEY,
            algorithm=settings.app.ALGORITHM,
        )
        return encoded_jwt

    # TODO: refactor
    @staticmethod
    def create_refresh_token(user_id: int):
        jwt_payload: RefreshTokenPayload = (
            RefreshTokenPayload(
                sub=str(user_id),
                iat=datetime.now(timezone.utc),
                exp=datetime.now(timezone.utc)
                + timedelta(minutes=settings.app.REFRESH_TOKEN_EXPIRE_MINUTES),
            )
            .model_dump()
            .copy()
        )
        encoded_jwt = jwt.encode(
            payload=jwt_payload,
            key=settings.app.SECRET_KEY,
            algorithm=settings.app.ALGORITHM,
        )
        return encoded_jwt

    @staticmethod
    def get_current_token_payload(
        credentials: Annotated[HTTPAuthorizationCredentials, Security(bearer_scheme)],
    ) -> dict:
        decoded_token = AuthHelper.decode_token(credentials.credentials)
        return decoded_token

    @staticmethod
    def decode_token(token: str) -> dict:
        try:
            payload = jwt.decode(
                token,
                settings.app.SECRET_KEY,
                algorithms=[settings.app.ALGORITHM],
            )
            if not payload or not payload.get("exp"):
                raise AuthHelper.credentials_exception
            if datetime.fromtimestamp(payload.get("exp"), timezone.utc) < datetime.now(
                timezone.utc
            ):
                raise HTTPException(
                    status_code=403,
                    detail="Token is expired",
                )
        except InvalidTokenError:
            raise AuthHelper.credentials_exception
        return payload
