from typing import Annotated

from fastapi import APIRouter, Depends, WebSocket, WebSocketException
from pydantic_core import ValidationError
from starlette import status
from starlette.websockets import WebSocketDisconnect

from app.dependencies.chat import get_current_websocket_auth_user
from app.schemas.messages import MessageCreate, WebsocketReceiveMessage
from app.schemas.users import UserSchema
from app.services.chats import ChatsService
from app.services.messages import MessagesService

router = APIRouter()


# TODO: Redis need to be connected
class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[int, set[WebSocket]] = {}

    async def connect(self, chat_id: int, ws: WebSocket):
        await ws.accept()
        self.active_connections.setdefault(chat_id, set()).add(ws)

    def disconnect(self, chat_id: int, ws: WebSocket):
        self.active_connections.get(chat_id, set()).discard(ws)

    async def broadcast(self, chat_id: int, data: dict):
        for ws in self.active_connections.get(chat_id, set()):
            await ws.send_json(data)


manager = ConnectionManager()


@router.websocket(
    "/ws/{chat_id}",
)
async def websocket_chat(
    chat_id: int,
    websocket: WebSocket,
    chats_service: Annotated[ChatsService, Depends(ChatsService)],
    messages_service: Annotated[MessagesService, Depends(MessagesService)],
    user: UserSchema = Depends(get_current_websocket_auth_user),
):
    # TODO: endure out to the ChatService
    if not await chats_service.is_member(chat_id=chat_id, user_id=user.id):
        await websocket.close(
            code=status.WS_1008_POLICY_VIOLATION,
            reason="Missing or invalid Authorization header",
        )

    await manager.connect(chat_id, websocket)

    try:
        while True:
            try:
                # Serializing the message
                received_json: dict = await websocket.receive_json()
                received_data = WebsocketReceiveMessage.model_validate(received_json)
                dto = MessageCreate(
                    chat_id=chat_id,
                    sender_id=user.id,
                    text=received_data.text,
                )

                # Save the message
                await messages_service.create_message(dto)
            except ValidationError:
                await websocket.close(
                    code=status.WS_1002_PROTOCOL_ERROR,
                    reason="Incorrect data format",
                )
                manager.disconnect(chat_id, websocket)
    except WebSocketDisconnect:
        manager.disconnect(chat_id, websocket)
