from typing import Any, List

from app import models, schemas, services
from app.api import dependencies
from app.core.config import settings
from app.models.group_model import Group
from app.services import group_service
from app.services.base_service import ModelType
from app.utils import send_new_account_email
from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/", response_model=List[schemas.GroupBase])
def get_groups(
   db: Session = Depends(dependencies.get_db),
   skip: int = 0,
   limit: int = 100,
    # current_group: models.Group = Depends(deps.get_current_active_supergroup),
) -> List[Group]:
    return group_service.get_multi(db, skip=skip, limit=limit)
    


@router.post("/", response_model=schemas.GroupBase)
def create_group(
   *,
   db: Session = Depends(dependencies.get_db),
   group_create: schemas.GroupCreate,
) -> Any:
   return group_service.create(db, group_create=group_create)
 


# @router.put("/me", response_model=schemas.Group)
# def update_group_me(
#     *,
#     db: Session = Depends(dependencies.get_db),
#     password: str = Body(None),
#     full_name: str = Body(None),
#     email: EmailStr = Body(None),
#     current_group: models.Group = Depends(dependencies.get_current_active_group),
# ) -> Any:
#     """
#     Update own group.
#     """
#     current_group_data = jsonable_encoder(current_group)
#     group_in = schemas.GroupUpdate(**current_group_data)
#     if password is not None:
#         group_in.password = password
#     if full_name is not None:
#         group_in.full_name = full_name
#     if email is not None:
#         group_in.email = email
#     group = services.group.update(db, db_obj=current_group, obj_in=group_in)
#     return group


# @router.get("/me", response_model=schemas.Group)
# def read_group_me(
#     db: Session = Depends(dependencies.get_db),
#     current_group: models.Group = Depends(dependencies.get_current_active_group),
# ) -> Any:
#     """
#     Get current group.
#     """
#     return current_group


# @router.post("/open", response_model=schemas.Group)
# def create_group_open(
#     *,
#     db: Session = Depends(dependencies.get_db),
#     password: str = Body(...),
#     email: EmailStr = Body(...),
#     full_name: str = Body(None),
# ) -> Any:
#     """
#     Create new group without the need to be logged in.
#     """
#     if not settings.USERS_OPEN_REGISTRATION:
#         raise HTTPException(
#             status_code=403,
#             detail="Open group registration is forbidden on this server",
#         )
#     group = services.group.get_by_email(db, email=email)
#     if group:
#         raise HTTPException(
#             status_code=400,
#             detail="The group with this groupname already exists in the system",
#         )
#     group_in = schemas.GroupCreate(password=password, email=email, full_name=full_name)
#     group = services.group.create(db, obj_in=group_in)
#     return group


# @router.get("/{group_id}", response_model=schemas.Group)
# def read_group_by_id(
#     group_id: int,
#     current_group: models.Group = Depends(dependencies.get_current_active_group),
#     db: Session = Depends(dependencies.get_db),
# ) -> Any:
#     """
#     Get a specific group by id.
#     """
#     group = services.group.get(db, id=group_id)
#     if group == current_group:
#         return group
#     if not services.group.is_admin(current_group):
#         raise HTTPException(
#             status_code=400, detail="The group doesn't have enough privileges"
#         )
#     return group


# @router.put("/{group_id}", response_model=schemas.Group)
# def update_group(
#     *,
#     db: Session = Depends(dependencies.get_db),
#     group_id: int,
#     group_in: schemas.GroupUpdate,
#     current_group: models.Group = Depends(dependencies.get_current_active_supergroup),
# ) -> Any:
#     """
#     Update a group.
#     """
#     group = services.group.get(db, id=group_id)
#     if not group:
#         raise HTTPException(
#             status_code=404,
#             detail="The group with this groupname does not exist in the system",
#         )
#     group = services.group.update(db, db_obj=group, obj_in=group_in)
#     return group
