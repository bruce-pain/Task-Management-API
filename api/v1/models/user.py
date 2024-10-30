"""User data model"""

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from api.v1.models.base_model import BaseTableModel


class User(BaseTableModel):
    __tablename__ = "users"

    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=True)
    username = Column(String, unique=True, nullable=True)

    tasks = relationship("Task", back_populates="creator")

    def to_dict(self):
        obj_dict = super().to_dict()
        obj_dict.pop("password")
        return obj_dict

    def __str__(self):
        return "User: {} {}".format(self.email, self.first_name)
