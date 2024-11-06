"""Task data model"""

from sqlalchemy import Column, String, DateTime, ForeignKey, ARRAY, Index
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
        String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    assigned_to = Column(
        String, nullable=True, index=True
    )  # Email of the assigned user
    tags = Column(ARRAY(String), nullable=True)

    # Relationship with User
    creator = relationship("User", back_populates="tasks")

    # Composite index on created_by and assigned_to
    __table_args__ = (Index("idx_created_by_assigned_to", "created_by", "assigned_to"),)

    def __repr__(self):
        return f"<Task(id={self.id}, title='{self.title}', status='{self.status}')>"
