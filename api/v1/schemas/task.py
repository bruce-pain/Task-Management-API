from pydantic import BaseModel, Field, EmailStr, StringConstraints
from typing import Optional, List, Annotated, Union
from datetime import datetime
from enum import Enum


class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in-progress"
    COMPLETED = "completed"


class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class CreateTask(BaseModel):
    title: Annotated[str, StringConstraints(min_length=1)] = Field(
        ..., description="The title of the task"
    )
    description: Optional[str] = Field(
        None, description="A detailed description of the task"
    )
    dueDate: datetime = Field(..., description="The date and time the task is due")
    status: TaskStatus = Field(
        TaskStatus.PENDING, description="The current status of the task"
    )
    priority: TaskPriority = Field(None, description="The priority level of the task")
    assigned_to: Optional[EmailStr] = Field(
        None, description="Email of the user assigned to the task"
    )
    tags: Optional[List[str]] = Field(
        None, description="List of tags associated with the task"
    )

    class Config:
        schema_extra = {
            "example": {
                "title": "Finish documentation",
                "description": "Complete the API documentation for the project",
                "due_date": "2023-12-15T15:00:00Z",
                "status": "pending",
                "priority": "high",
                "assigned_to": "assignee@example.com",
                "tags": ["documentation", "high-priority"],
            }
        }


class UpdateTask(BaseModel):
    title: Optional[Annotated[str, StringConstraints(min_length=1)]] = Field(
        None, description="The title of the task"
    )
    description: Optional[str] = Field(
        None, description="A detailed description of the task"
    )
    due_date: Optional[datetime] = Field(
        None, description="The date and time the task is due"
    )
    status: Optional[TaskStatus] = Field(
        None, description="The current status of the task"
    )
    priority: Optional[TaskPriority] = Field(
        None, description="The priority level of the task"
    )
    assigned_to: Optional[EmailStr] = Field(
        None, description="Email of the user assigned to the task"
    )
    tags: Optional[List[str]] = Field(
        None, description="List of tags associated with the task"
    )

    class Config:
        schema_extra = {
            "example": {
                "title": "Finish documentation",
                "description": "Update the API documentation based on new endpoints",
                "due_date": "2023-12-15T15:00:00Z",
                "status": "in-progress",
                "priority": "medium",
                "assigned_to": "assignee@example.com",
                "tags": ["documentation", "update"],
            }
        }


class TaskBaseResponse(BaseModel):
    id: str = Field(..., description="Unique identifier for the task")
    title: str = Field(..., description="Title of the task")
    description: Optional[str] = Field(
        None, description="Detailed description of the task"
    )
    due_date: datetime = Field(..., description="The due date and time for the task")
    status: TaskStatus = Field(..., description="Current status of the task")
    priority: Optional[TaskPriority] = Field(
        None, description="Priority level of the task"
    )
    created_at: datetime = Field(..., description="Timestamp when the task was created")
    updated_at: datetime = Field(..., description="Timestamp of the last update")
    created_by: str = Field(..., description="ID of the user who created the task")
    assigned_to: Optional[EmailStr] = Field(
        None, description="Email of the assigned user"
    )
    tags: Optional[List[str]] = Field(None, description="Tags associated with the task")


class ResponseWrapper(BaseModel):
    status_code: int = Field(..., description="HTTP status code")
    detail: str = Field(..., description="Response message")
    data: Union[TaskBaseResponse, List[TaskBaseResponse], dict, None] = Field(
        ..., description="Response data"
    )

    class Config:
        schema_extra = {
            "example": {
                "status_code": 200,
                "detail": "Request successful",
                "data": None,
            }
        }


# Response for task creation
class CreateTaskResponse(ResponseWrapper):
    data: TaskBaseResponse = Field(..., description="Details of the created task")

    class Config:
        schema_extra = {
            "example": {
                "status_code": 201,
                "detail": "Task successfully created.",
                "data": TaskBaseResponse.Config.schema_extra["example"],
            }
        }


# Response for task update
class UpdateTaskResponse(ResponseWrapper):
    data: TaskBaseResponse = Field(..., description="Details of the updated task")

    class Config:
        schema_extra = {
            "example": {
                "status_code": 200,
                "detail": "Task successfully updated.",
                "data": TaskBaseResponse.Config.schema_extra["example"],
            }
        }


# Response for a detailed view of a single task
class TaskDetailResponse(ResponseWrapper):
    data: TaskBaseResponse = Field(..., description="Details of the task")

    class Config:
        schema_extra = {
            "example": {
                "status_code": 200,
                "detail": "Task details retrieved successfully.",
                "data": TaskBaseResponse.Config.schema_extra["example"],
            }
        }


# Response for a list of tasks
class TaskListResponse(ResponseWrapper):
    data: dict = Field(..., description="Paginated list of tasks")

    class Config:
        schema_extra = {
            "example": {
                "status_code": 200,
                "detail": "Tasks retrieved successfully.",
                "data": {
                    "tasks": [TaskBaseResponse.Config.schema_extra["example"]],
                    "total": 100,
                    "page": 1,
                    "limit": 10,
                },
            }
        }
