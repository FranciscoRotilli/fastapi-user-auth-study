from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey, Table, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum

from ..database import Base

class CaseStatus(str, Enum):
    OPEN = "open"
    CLOSED = "closed"
    CANCELED = "canceled"

case_user_association = Table(
    'case_user_association', Base.metadata,
    Column('case_id', Integer, ForeignKey('cases.id'), primary_key=True),
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True)
)

class Case(Base):
    __tablename__ = "cases"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    case_number = Column(String, index=True, unique=True, nullable=False)

    status = Column(SQLAlchemyEnum(CaseStatus), default=CaseStatus.OPEN, nullable=False)

    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="owned_cases")

    authorized_users = relationship(
        "User",
        secondary=case_user_association,
        back_populates="accessible_cases"
    )

    class Config:
        orm_mode = True
