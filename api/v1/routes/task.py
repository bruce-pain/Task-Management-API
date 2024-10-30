from typing import Annotated
from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from api.db.database import get_db
from api.core.dependencies.security import get_current_user
from api.v1.models.user import User
from api.v1.schemas import task as TaskSchema
from api.v1.services import task as TaskService

task_router = APIRouter(prefix="/tasks", tags=["Tasks"])


@task_router.post(
    path="",
    response_model=TaskSchema.CreateTaskResponse,
    status_code=status.HTTP_200_OK,
    summary="Create a new task",
    description="This endpoint creates a new task",
    tags=["Tasks"],
)
def create_task(
    schema: TaskSchema.CreateTask,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> TaskSchema.CreateTaskResponse:
    return TaskService.create(db, schema, current_user)
