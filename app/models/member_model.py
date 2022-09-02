

from uuid import uuid4

from app.core.security import get_password_hash
from app.db.base_class import Base
from sqlalchemy import Boolean, Column, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP


class Member():
   member_id=Column(String, ForeignKey("user.id"), primary_key=True, index=True,default=str(uuid4()))
   group_id=Column(String, ForeignKey("groups.id"), primary_key=True, index=True,default=str(uuid4()))
   created_at=Column(TIMESTAMP(timezone=True), nullable=False,server_default=text('now()'))
   member=relationship('Users')
   group=relationship('Groups')
