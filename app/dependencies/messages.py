from fastapi import Depends, HTTPException, Path
from starlette import status

from app.dependencies.users import get_current_auth_user
from app.repositories.chats import ChatsRepository
from app.schemas.users import UserSchema


async def ensure_user_is_member(
    chat_id: int = Path(...),
    current_user: UserSchema = Depends(get_current_auth_user),
    chats_repository: ChatsRepository = Depends(ChatsRepository),
) -> bool:
    if not await chats_repository.is_member(chat_id=chat_id, user_id=current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a member of this chat.",
        )
    return True
