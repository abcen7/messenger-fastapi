from fastapi import HTTPException
from fastapi.params import Depends
from starlette import status

from app.auth.schemas import TokenPayload
from app.auth.utils import AuthHelper
from app.users.repositories import UsersRepository
from app.users.schemas import UserLogin, UserSchema
from app.utils.constants import ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE, TOKEN_TYPE_FIELD


async def validate_auth_user(
    user_login: UserLogin,
    users_repository: UsersRepository = Depends(UsersRepository),
) -> UserSchema:
    if (user := await users_repository.get_one_by_email(user_login.email)) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    if not AuthHelper.verify_password(user_login.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid credentials",
        )
    return UserSchema.model_validate(user, from_attributes=True)


async def get_user_by_token_sub(
    payload: dict, users_repository: UsersRepository
) -> UserSchema:
    print(payload)
    if user := await users_repository.get_one(int(payload.get("sub"))):
        return UserSchema.model_validate(user, from_attributes=True)
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token is invalid",
    )


def validate_token_type(
    payload: dict,
    token_type: str,
) -> bool:
    current_token_type = payload.get(TOKEN_TYPE_FIELD)
    if current_token_type == token_type:
        return True
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Invalid token type {current_token_type!r} expected {token_type!r}",
    )


class UserGetterFromToken:
    def __init__(self, token_type: str):
        self.token_type = token_type

    async def __call__(
        self,
        payload: dict = Depends(AuthHelper.get_current_token_payload),
        users_repository: UsersRepository = Depends(UsersRepository),
    ) -> UserSchema:
        validate_token_type(payload, self.token_type)
        return await get_user_by_token_sub(payload, users_repository)


get_current_auth_user = UserGetterFromToken(ACCESS_TOKEN_TYPE)
get_current_auth_user_for_refresh = UserGetterFromToken(REFRESH_TOKEN_TYPE)
