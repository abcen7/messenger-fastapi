from fastapi import APIRouter

from app.api.rest.v1 import auth_router, chats_router, messages_router, users_router
from app.api.websocket.v1 import websocket_router

api_router = APIRouter(prefix="/api/v1")

REST_API_ROUTERS = [
    users_router,
    auth_router,
    messages_router,
    chats_router,
]

WEBSOCKET_API_ROUTERS = [websocket_router]

INCLUDED_ROUTERS = [
    *REST_API_ROUTERS,
    *WEBSOCKET_API_ROUTERS,
]

for ROUTER in INCLUDED_ROUTERS:
    api_router.include_router(ROUTER)
