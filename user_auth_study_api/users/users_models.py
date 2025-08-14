from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship
from enum import Enum

from ..database import Base
from ..cases.cases_models import case_user_association

class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(String, default=UserRole.USER, nullable=False)

    owned_cases = relationship("Case", back_populates="owner")
    accessible_cases = relationship(
        "Case",
        secondary=case_user_association,
        back_populates="authorized_users"
    )

    class Config:
        orm_mode = True