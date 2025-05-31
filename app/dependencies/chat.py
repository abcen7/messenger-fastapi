from typing import Annotated

from fastapi import Depends, WebSocket, WebSocketException
from starlette import status

from app.dependencies.users import get_user_by_token_sub, validate_token_type
from app.repositories.users import UsersRepository
from app.schemas.users import UserSchema
from app.utils.auth import AuthHelper
from app.utils.constants import ACCESS_TOKEN_TYPE, BEARER_TOKEN_TYPE


async def get_current_websocket_auth_user(
    websocket: WebSocket,
    users_repository: Annotated[UsersRepository, Depends()],
) -> UserSchema:
    # get auth header
    auth_header = websocket.headers.get("Authorization")
    if not auth_header or not auth_header.startswith(f"{BEARER_TOKEN_TYPE} "):
        raise WebSocketException(
            code=status.WS_1008_POLICY_VIOLATION,
            reason="Missing or invalid Authorization header",
        )

    # extract token from auth header
    token = auth_header.split(" ", 1)[1]

    try:
        payload: dict = AuthHelper.decode_token(token)
    except Exception:
        raise WebSocketException(
            code=status.WS_1008_POLICY_VIOLATION,
            reason="Invalid or expired token",
        )

    validate_token_type(payload, ACCESS_TOKEN_TYPE)

    # get user by sub
    user = await get_user_by_token_sub(payload, users_repository)
    return user
