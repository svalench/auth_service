from email_validator import validate_email
from typing import Optional
import re

from fastapi import HTTPException
from pydantic import BaseModel, validator
from starlette import status


class UserSchema(BaseModel):
    """Pydantic Schema"""
    id: Optional[str]
    username: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    password: str
    is_admin: Optional[bool]

    @validator("phone")
    def check_phoneNumber_format(cls, v):
        if v:
            regExs = (r"\(\w{3}\) \w{3}\-\w{4}", r"^\w{3}\-\w{4}$")
            if not re.search(regExs[0], v):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="not valid phone")
        return v

    @validator("email")
    def validate_email_user(cls, v):
        if v:
            try:
                emailObject = validate_email(v)
                return emailObject.email
            except Exception as e:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Error validate email: {str(e)}')
        return v

    class Config:
        orm_mode = True