from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from .users_models import User
from .users_schemas import UserResponse, UserCreate
from ..auth.auth_router import require_admin_role
from . import users_service

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Creates a new user in the database after validating email and username uniqueness.
    Args:
        user (UserCreate): The user data to create, including email and username.
        db (Session, optional): The database session dependency.
    Raises:
        HTTPException: If the email is already in use.
        HTTPException: If the username is already in use.
    Returns:
        User: The newly created user object.
    """

    db_user_by_email = users_service.get_user_by_email(db, email=user.email)
    if db_user_by_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already in use."
        )
    db_user_by_username = users_service.get_user_by_username(db, username=user.username)
    if db_user_by_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already in use."
        )
    
    new_user = users_service.create_user(db=db, user=user)
    return new_user

@router.get("/", response_model=List[UserResponse])
def read_all_users(db: Session = Depends(get_db), current_user: UserResponse = Depends(require_admin_role)):
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