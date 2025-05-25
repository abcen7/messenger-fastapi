from fastapi import APIRouter

from app.auth.api.v1 import auth_router
from app.users.api.v1 import users_router

api_router = APIRouter(prefix="/api/v1")

INCLUDED_ROUTERS = [
    users_router,
    auth_router,
]

for ROUTER in INCLUDED_ROUTERS:
    api_router.include_router(ROUTER)
