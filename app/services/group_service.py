from datetime import timedelta
from http.client import HTTPException
from typing import Any, Dict, Optional, Union

from app.core import security
from app.core.config import settings
from app.core.security import get_password_hash, verify_password
from app.models import Group
from app.schemas import GroupBase, GroupCreate, GroupUpdate
from app.schemas.token import Token
from app.services.base_service import CRUDBase
from sqlalchemy.orm import Session


class CRUDGroup(CRUDBase[Group, GroupCreate, GroupUpdate]):
    def create(self, db: Session, *, group_create: GroupCreate) -> Group:
        print("==================group_create", group_create)
        existed_group = db.query(self.model).filter(self.model.creator_id == group_create.creator_id and self.model.name == group_create.name).first()
        if existed_group:
            raise HTTPException(
                status_code=400,
                detail=f"The group with name {group_create.name} already exists in the system.",
            )
        created_group = Group(**group_create)
        db.add(created_group)
        db.commit()
        db.refresh(created_group)
        return created_group

    # def update(
    #     self, db: Session, *, db_obj: group, obj_in: Union[UserUpdate, Dict[str, Any]]
    # ) -> group:
    #     if isinstance(obj_in, dict):
    #         update_data = obj_in
    #     else:
    #         update_data = obj_in.dict(exclude_unset=True)
    #     if update_data["password"]:
    #         hashed_password = get_password_hash(update_data["password"])
    #         del update_data["password"]
    #         update_data["hashed_password"] = hashed_password
    #     return super().update(db, db_obj=db_obj, obj_in=update_data)

  

group_service = CRUDGroup(Group)
