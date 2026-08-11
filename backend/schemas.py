from pydantic import BaseModel, EmailStr
from typing import Optional

# 1. Schema for Registration
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    role: str
    parent_id: Optional[int] = None

# 2. Schema for Login (This was missing!)
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# 3. Schema for Token Response
class Token(BaseModel):
    access_token: str
    token_type: str
    role: str
    full_name: str
    user_id: int

# 4. Schema for Output User Data
class UserOut(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    role: str

    class Config:
        from_attributes = True