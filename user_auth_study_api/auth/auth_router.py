from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from ..database import get_db
from ..config import settings
from . import auth_service, auth_schemas
from ..users import users_service, users_schemas

router = APIRouter(
    tags=["authentication"]
)

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/token")

async def get_current_user(token: str = Depends(oauth2_schema), db: Session = Depends(get_db)):
    """
    Retrieve the current authenticated user based on the provided JWT token.
    Args:
        token (str): JWT token extracted from the request using OAuth2 schema.
        db (Session): SQLAlchemy database session dependency.
    Returns:
        User: The authenticated user object.
    Raises:
        HTTPException: If the token is invalid, expired, or the user does not exist.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unable to validate credentials.",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = auth_schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    user = users_service.get_user_by_username(db, username=str(token_data.username))
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: users_schemas.UserResponse = Depends(get_current_user)):
    """
    Retrieve the current active user.
    Args:
        current_user (users_schemas.UserResponse): The currently authenticated user, provided by the get_current_user dependency.
    Raises:
        HTTPException: If the user is not active.
    Returns:
        users_schemas.UserResponse: The current active user.
    """
    
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user.")
    return current_user

@router.post("/token", response_model=auth_schemas.Token)
async def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = auth_service.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = auth_service.create_access_token(data={"sub": user.username})

    return {"access_token": access_token, "token_type": "bearer"}