from sqlalchemy.orm import Session
from fastapi import status, HTTPException
from starlette.status import HTTP_200_OK

from api.v1.models.user import User
from api.v1.models.task import Task as TaskModel
from api.v1.schemas import task as TaskSchema


def model_to_schema(task: TaskModel) -> TaskSchema.TaskBaseResponse:
    return TaskSchema.TaskBaseResponse(
        id=task.id,
        title=task.title,
        description=task.description,
        due_date=task.due_date,
        status=task.status,
        priority=task.priority,
        created_at=task.created_at,
        updated_at=task.updated_at,
        created_by=task.created_by,
        assigned_to=task.assigned_to,
        tags=task.tags,
    )


def create(
    db: Session, schema: TaskSchema.CreateTask, current_user: User
) -> TaskSchema.CreateTaskResponse:
    new_task = TaskModel(**schema.model_dump())
    new_task.created_by = current_user.id

    try:
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create task {e}",
        ) from e

    response_data = model_to_schema(new_task)
    return TaskSchema.CreateTaskResponse(
        status_code=status.HTTP_201_CREATED,
        detail="Task successfully created.",
        data=response_data,
    )


def fetch(
    db: Session, current_user: User, task_id: str
) -> TaskSchema.TaskDetailResponse:
    retrieved_task = db.get(entity=TaskModel, ident=task_id)

    if not retrieved_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found."
        )

    # check if task is related to current user
    if (retrieved_task.created_by != current_user.id) and (
        retrieved_task.assigned_to != current_user.email
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this Task.",
        )

    response_data = model_to_schema(retrieved_task)

    return TaskSchema.TaskDetailResponse(
        status_code=HTTP_200_OK,
        detail="Task successfully retrieved.",
        data=response_data,
    )
