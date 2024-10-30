"""Task data model"""

from sqlalchemy import Column, String, DateTime, ForeignKey, ARRAY
from sqlalchemy.orm import relationship
from api.v1.models.base_model import BaseTableModel


class Task(BaseTableModel):
    __tablename__ = "tasks"

    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    due_date = Column(DateTime, nullable=False)
    status = Column(String, nullable=False)
    priority = Column(String, nullable=True)
    created_by = Column(
        String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    assigned_to = Column(String, nullable=True)  # Email of the assigned user
    tags = Column(ARRAY(String), nullable=True)

    # Relationship with User
    creator = relationship("User", back_populates="tasks")

    def __repr__(self):
        return f"<Task(id={self.id}, title='{self.title}', status='{self.status}')>"
