from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from ..database import get_db
from .users_models import User
from .users_schemas import UserResponse, UserCreate
from ..auth import auth_router
from . import users_service
from .users_schemas import Role

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_new_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(auth_router.try_get_current_user)
    ):
    """
    """

    db_user_by_email = users_service.get_user_by_email(db, email=user_data.email)
    if db_user_by_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already in use."
        )
    db_user_by_username = users_service.get_user_by_username(db, username=user_data.username)
    if db_user_by_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already in use."
        )
    
    is_admin_creation = current_user is not None and getattr(current_user, "role", None) == Role.ADMIN

    if not is_admin_creation:
        user_data.role = Role.USER

    new_user = users_service.create_user(db=db, user=user_data)
    return new_user

@router.get("/", response_model=List[UserResponse])
def read_all_users(db: Session = Depends(get_db), current_user: UserResponse = Depends(auth_router.require_admin_role)):
    """
    Retrieve all users (admin only).
    Args:
        db (Session): SQLAlchemy database session dependency.
        current_user (UserResponse): The currently authenticated admin user.
    Returns:
        List[users_schemas.UserResponse]: List of all users.
    """
    users = users_service.get_all_users(db)
    return users