import uuid

from fastapi_viewsets.db_conf import Base
from sqlalchemy import Column, String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import relationship


class User(Base):
    """SQLAlchemy model"""

    __tablename__ = "user"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String, unique=True)
    password = Column(String(255))
    phone = Column('phone', String(255), unique=True)
    email = Column('email', String(255), unique=True)
    address = Column(String(255))
    is_admin = Column(Boolean, default=False)
    emails = relationship("Emails")


class Emails(Base):

    __tablename__ = "emails"

    id = Column(Integer, primary_key=True)
    parent_id = Column(String, ForeignKey("user.id"))
    email = Column('email', String(255), unique=True)
