from app.api.routers import group_router, login_router, user_router
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(login_router.router, tags=["login"])
api_router.include_router(user_router.router, prefix="/users", tags=["users"])
# api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(group_router.router, prefix="/groups", tags=["groups"])


