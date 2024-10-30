from sqlalchemy.orm import Session
from sqlalchemy import desc, or_
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
    retrieved_task = (
        db.query(TaskModel)
        .filter(TaskModel.id == task_id)
        .filter(
            or_(
                TaskModel.created_by == current_user.id,
                TaskModel.assigned_to == current_user.email,
            )
        )
        .first()
    )

    if not retrieved_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found."
        )

    response_data = model_to_schema(retrieved_task)

    return TaskSchema.TaskDetailResponse(
        status_code=HTTP_200_OK,
        detail="Task successfully retrieved.",
        data=response_data,
    )


def fetch_list(
    db: Session, current_user: User, page: int, limit: int
) -> TaskSchema.TaskListResponse:
    # get all tasks related to current_user
    all_tasks = db.query(TaskModel).filter(
        or_(
            TaskModel.created_by == current_user.id,
            TaskModel.assigned_to == current_user.email,
        )
    )

    total_tasks: int = all_tasks.count()
    total_pages: int = int(total_tasks / limit) + (total_tasks % limit > 0)

    paginated_tasks = (
        all_tasks.order_by(desc(TaskModel.created_by))
        .limit(limit)
        .offset((page - 1) * limit)
        .all()
    )

    task_list = [model_to_schema(task) for task in paginated_tasks]

    response_data = TaskSchema.TaskListData(
        tasks=task_list,
        total=total_tasks,
        totalPages=total_pages,
        page=page,
        limit=limit,
    )

    return TaskSchema.TaskListResponse(
        status_code=status.HTTP_200_OK,
        detail="Tasks successfully retrieved.",
        data=response_data,
    )


def update(
    db: Session, current_user: User, task_id: str, schema: TaskSchema.UpdateTask
) -> TaskSchema.UpdateTaskResponse:
    retrieved_task = (
        db.query(TaskModel)
        .filter(TaskModel.id == task_id)
        .filter(
            or_(
                TaskModel.created_by == current_user.id,
                TaskModel.assigned_to == current_user.email,
            )
        )
        .first()
    )

    if not retrieved_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found."
        )

    update_data = schema.model_dump(exclude_unset=True)

    # replace task data with updated data
    for key, value in update_data.items():
        setattr(retrieved_task, key, value)

    try:
        db.commit()
        db.refresh(retrieved_task)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update task {e}",
        ) from e

    response_data = model_to_schema(retrieved_task)

    return TaskSchema.UpdateTaskResponse(
        status_code=status.HTTP_200_OK,
        detail="Task successfully updated.",
        data=response_data,
    )


def delete(db: Session, current_user: User, task_id: str) -> None:
    retrieved_task = (
        db.query(TaskModel)
        .filter(TaskModel.id == task_id)
        .filter(
            or_(
                TaskModel.created_by == current_user.id,
                TaskModel.assigned_to == current_user.email,
            )
        )
        .first()
    )

    if not retrieved_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found."
        )

    try:
        db.delete(retrieved_task)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete task {e}",
        ) from e
