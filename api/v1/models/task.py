"""Task data model"""

from sqlalchemy import Column, String, DateTime, Enum, ForeignKey, ARRAY
from sqlalchemy.orm import relationship
from api.v1.models.base_model import BaseTableModel
from enum import Enum as PyEnum


class TaskStatus(PyEnum):
    PENDING = "pending"
    IN_PROGRESS = "in-progress"
    COMPLETED = "completed"


class TaskPriority(PyEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Task(BaseTableModel):
    __tablename__ = "tasks"

    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    due_date = Column(DateTime, nullable=False)
    status = Column(Enum(TaskStatus), default=TaskStatus.PENDING, nullable=False)
    priority = Column(Enum(TaskPriority), nullable=True)
    created_by = Column(
        String, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    assigned_to = Column(String, nullable=True)  # Email of the assigned user
    tags = Column(ARRAY(String), nullable=True)

    # Relationship with User
    creator = relationship("User", back_populates="tasks")

    def __repr__(self):
        return f"<Task(id={self.id}, title='{self.title}', status='{self.status}')>"
