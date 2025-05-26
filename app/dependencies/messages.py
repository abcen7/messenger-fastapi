from fastapi import Depends, Path

from app.dependencies.users import get_current_auth_user
from app.schemas.users import UserSchema


async def ensure_user_in_chat(
    chat_id: int = Path(...),
    current_user: UserSchema = Depends(get_current_auth_user),
):
    pass
