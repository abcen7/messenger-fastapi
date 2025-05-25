from fastapi import APIRouter

from app.api.rest.v1 import auth_router, users_router

api_router = APIRouter(prefix="/api/v1")

INCLUDED_ROUTERS = [
    users_router,
    auth_router,
]

for ROUTER in INCLUDED_ROUTERS:
    api_router.include_router(ROUTER)
