import uuid

from fastapi_viewsets.db_conf import Base
from sqlalchemy import Column, String, Boolean


class User(Base):
    """SQLAlchemy model"""

    __tablename__ = "user"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String, unique=True)
    password = Column(String(255))
    email = Column(String(255))
    phone = Column(String(255))
    is_admin = Column(Boolean, default=False)
