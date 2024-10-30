from fastapi import APIRouter

from api.v1.routes.auth import auth
from api.v1.routes.task import task_router

main_router = APIRouter(prefix="/api/v1")

main_router.include_router(router=auth)
main_router.include_router(router=task_router)
