from pydantic import BaseModel, EmailStr, Field, model_validator
from typing import Optional
from enum import Enum
import re
from typing import Annotated

class UserRole(str, Enum):
    architect = "Architect"
    customer = "Customer"
    engineer = "Engineer"
    supplier = "Supplier"

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
    role: UserRole
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
    id: int
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: str
    disabled: Optional[bool] = False

    class Config:
        from_attributes = True

class UserInDB(BaseModel):
    id: int
    email: EmailStr
    hashed_password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: str
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