from email_validator import validate_email
from typing import Optional, List
import re

from fastapi import HTTPException
from pydantic import BaseModel, validator
from starlette import status


class EmailsSchema(BaseModel):
    """email schema"""
    id: Optional[str]
    parent_id: str
    email: Optional[str] = None

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


class PhonesSchema(BaseModel):
    """email schema"""
    phone: Optional[str] = None

    @validator("phone")
    def check_phone_number_format(cls, v):
        if v:
            regExs = (r"\(\w{3}\) \w{3}\-\w{4}", r"^\w{3}\-\w{4}$")
            if not re.search(regExs[0], v):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="not valid phone")
        return v

    class Config:
        orm_mode = True


class UserSchema(BaseModel):
    """Pydantic user Schema"""
    id: Optional[str]
    username: Optional[str] = None
    address: Optional[str] = None
    password: str
    phones: Optional[List[PhonesSchema]] = None
    emails: Optional[List[EmailsSchema]] = None
    is_admin: Optional[bool]

    class Config:
        orm_mode = True
