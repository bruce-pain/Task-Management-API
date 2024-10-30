from typing import Annotated
from fastapi import APIRouter, Query, status, Depends
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
    status_code=status.HTTP_201_CREATED,
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


@task_router.get(
    path="/{task_id}",
    response_model=TaskSchema.TaskDetailResponse,
    status_code=status.HTTP_200_OK,
    summary="Fetch a single task by id",
    description="This endpoint fetches a single task by it's ID and returns the task details",
    tags=["Tasks"],
)
def fetch_task_by_id(
    task_id: str,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> TaskSchema.TaskDetailResponse:
    return TaskService.fetch(db, current_user, task_id)


@task_router.get(
    path="",
    response_model=TaskSchema.TaskListResponse,
    status_code=status.HTTP_200_OK,
    summary="Fetch all tasks",
    description="This endpoint fetches a paginated list of all tasks related to the current user",
    tags=["Tasks"],
)
def fetch_all_tasks(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
    page: int = 1,
    limit: int = 10,
) -> TaskSchema.TaskListResponse:
    return TaskService.fetch_list(db, current_user, page, limit)
