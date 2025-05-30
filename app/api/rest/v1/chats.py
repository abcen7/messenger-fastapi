from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status

from app.dependencies.users import get_current_auth_user
from app.schemas.chats import ChatCreate
from app.schemas.users import UserSchema
from app.services.chats import ChatsService

router = APIRouter(
    prefix="/chats",
    tags=["Chats"],
    dependencies=[Depends(get_current_auth_user)],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_chat(
    chat: ChatCreate,
    chats_service: Annotated[ChatsService, Depends()],
    current_user: Annotated[UserSchema, Depends(get_current_auth_user)],
):
    return await chats_service.create(current_user.id, chat)


@router.get("/")
async def get_all_chats():
    pass


@router.get("/{chat_id}")
async def get_chat(chat_id: int):
    pass
