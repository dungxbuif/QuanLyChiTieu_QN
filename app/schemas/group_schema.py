from typing import Optional

from pydantic import BaseModel

from .user import User


# Shared properties
class GroupBase(BaseModel):
   name: Optional[str] = None
   slug: Optional[str] = None
   creator_id: Optional[str] = None
   creator: Optional[User] = None


# Properties to receive via API on creation
class GroupCreate(GroupBase):
   name: str
   creator_id: str 

# Properties to receive via API on update
class GroupUpdate(GroupBase):
   name: str


# class UserInDBBase(UserBase):
#     id: Optional[str] = None

#     class Config:
#         orm_mode = True


# # Additional properties to return via API
# class User(UserInDBBase):
#     pass


# # Additional properties stored in DB
# class UserInDB(UserInDBBase):
#     hashed_password: str
