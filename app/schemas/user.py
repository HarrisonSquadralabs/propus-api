from pydantic import BaseModel, EmailStr, Field, model_validator
from typing import Optional
from enum import Enum
from app.models.role import RoleType
import re
from typing import Annotated
from uuid import UUID

def validate_password(pw: str):
    if len(pw) < 8:
        raise ValueError("Password must be at least 8 characters long")
    if not re.search(r"[A-Z]", pw):
        raise ValueError("Password must include at least one uppercase letter")
    if not re.search(r"[a-z]", pw):
        raise ValueError("Password must include at least one lowercase letter")
    if not re.search(r"\d", pw):
        raise ValueError("Password must include at least one number")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", pw):
        raise ValueError("Password must include at least one special character")

 

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    confirm_password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: RoleType 
    architect_info: Optional[str] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    address: Optional[str] = None

    @model_validator(mode='before')
    def check_passwords_match(cls, values):
        pw = values.get('password')
        cpw = values.get('confirm_password')
        if pw != cpw:
            raise ValueError("Passwords do not match")
        validate_password(pw)
        return values

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserPublic(BaseModel):
    id: UUID  # <- cambiado de int a UUID
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role_name: str  # <- agregado
    disabled: Optional[bool] = False

    class Config:
        from_attributes = True

class UserInDB(BaseModel):
    id: UUID  
    email: EmailStr
    hashed_password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role_name: str  
    disabled: Optional[bool] = False

    class Config:
        from_attributes = True

class NewPassword(BaseModel):
    token: str
    new_password: Annotated[str, Field(min_length=6)]
    confirm_password: Annotated[str, Field(min_length=6)]

    @model_validator(mode='before')
    def passwords_match(cls, values):
        new_password = values.get('new_password')
        confirm_password = values.get('confirm_password')
        if new_password != confirm_password:
            raise ValueError('Las contraseñas no coinciden')
        return values

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_completed: Optional[bool] = None

    class Config:
        orm_mode = True

class UserRead(BaseModel):
    id: UUID
    email: EmailStr
    first_name: str
    last_name: str
    is_completed: bool
    role_id: UUID
    role_name: str 

    class Config:
        orm_mode = True
