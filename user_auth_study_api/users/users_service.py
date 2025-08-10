from sqlalchemy.orm import Session
from ..auth import auth_service as AuthService
from .users_models import User
from .users_schemas import UserCreate

def get_user_by_username(db: Session, username: str):
    """
    Fetches a user record from the database based on the provided username.

    Args:
        db (Session): SQLAlchemy database session.
        username (str): The username of the user to retrieve.

    Returns:
        User or None: The User object if found, otherwise None.
    """
    return db.query(User).filter(User.username == username).first()

def get_user_by_email(db: Session, email: str):
    """
    Fetches a user record from the database based on the provided email.

    Args:
        db (Session): SQLAlchemy database session.
        email (str): The email of the user to retrieve.

    Returns:
        User or None: The User object if found, otherwise None.
    """
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate):
    hashed_password = AuthService.get_password_hash(user.password)

    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user