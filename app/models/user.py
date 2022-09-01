

from app.core.security import get_password_hash
from app.db.base_class import Base
from sqlalchemy import Boolean, Column, String, event


class User(Base):
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    is_admin = Column(Boolean(), default=False)

    def hash_password(self, password):
        self.password = get_password_hash(password)

    def check_password(self, password):
        return get_password_hash(self.password_hash, password)

