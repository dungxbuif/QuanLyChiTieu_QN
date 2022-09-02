

from app.core.security import get_password_hash
from app.db.base_class import Base
from sqlalchemy import Boolean, Column, ForeignKey, String
from sqlalchemy.orm import relationship


class Group(Base):
   name=Column(String, nullable=False)
   slug=Column(String, unique=True, index=True, nullable=False)
   creator_id=Column(String, ForeignKey("users.id"), index=True, nullable=False)
   creator=relationship("User")
