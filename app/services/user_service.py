from datetime import timedelta
from http.client import HTTPException
from typing import Any, Dict, Optional, Union

from app.core import security
from app.core.config import settings
from app.core.security import get_password_hash, verify_password
from app.models.user_model import User
from app.schemas.token import Token
from app.schemas.user import UserCreate, UserUpdate
from app.services.base_service import CRUDBase
from sqlalchemy.orm import Session


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email_or_username(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first() if email.find('@') else db.query(User).filter(User.username == email)

    def create(self, db: Session, *, user_create: UserCreate) -> User:
        created_user = User(
            **user_create,
            password=get_password_hash(user_create.password),
            is_admin=False,
        )
        db.add(created_user)
        db.commit()
        db.refresh(created_user)
        return created_user

    def create_admin(self, db: Session,):
        email = settings.ADMIN_ACCOUNT
        admin_user = self.get_by_email_or_username(db, email=email)
        if not admin_user:
            password = settings.ADMIN_PASSWORD
            username = email.split('@')[0]
            admin_user = User(
                email = email,
                username = username,
                is_admin = True
            )
            admin_user.hash_password(password)
            db.add(admin_user)
            db.commit()
            db.refresh(admin_user)
        print('Create admin successfully!')
    
    def update(
        self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(self, db: Session, *, email: str, password: str) -> Token:
        user = self.get_by_email_or_username(db, email=email)
        if not user:
            raise HTTPException(status_code=400, detail="Incorrect email or password")
        if not user.is_active(user):
            raise HTTPException(status_code=400, detail="Inactive user")
        if not verify_password(password, user.hashed_password):
            return None
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        return { 
            "access_token": security.create_access_token(
                user.id, expires_delta=access_token_expires
            ),
            "token_type": "bearer",
        }

    def is_active(self, user: User) -> bool:
        return user.is_active

    def is_admin(self, user: User) -> bool:
        return user.is_admin


user_service = CRUDUser(User)
