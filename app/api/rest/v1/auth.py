from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status

from app.auth.schemas import TokenPair
from app.auth.utils import AuthHelper
from app.dependencies.users import get_current_auth_user_for_refresh, validate_auth_user
from app.schemas.users import UserSchema

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    response_model=TokenPair,
)
async def auth_user_issue_jwt(
    user: Annotated[UserSchema, Depends(validate_auth_user)],
) -> TokenPair:
    access_token = AuthHelper.create_access_token(user_id=user.id)
    refresh_token = AuthHelper.create_refresh_token(user_id=user.id)
    return TokenPair(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.post(
    "/refresh",
    status_code=status.HTTP_200_OK,
    response_model=TokenPair,
)
async def auth_refresh_jwt(
    user: Annotated[UserSchema, Depends(get_current_auth_user_for_refresh)],
) -> TokenPair:
    access_token = AuthHelper.create_access_token(user_id=user.id)
    refresh_token = AuthHelper.create_refresh_token(user_id=user.id)
    return TokenPair(
        access_token=access_token,
        refresh_token=refresh_token,
    )
