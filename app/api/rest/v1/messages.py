from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status

from app.dependencies.messages import ensure_user_is_member
from app.services.messages import MessagesService

router = APIRouter(prefix="/messages", tags=["Messages"])


@router.get(
    "/history/{chat_id}",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(ensure_user_is_member)],
)
async def get_history_messages(
    messages_service: Annotated[MessagesService, Depends()],
    chat_id: int,
):
    return await messages_service.get_history(chat_id)
