from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: Optional[str] = None

#Response Schema
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


#response schema for owner account
class OwnerOut(UserOut):
    role: str

    class Config:
        from_attributes = True


class BookCreate(BaseModel):
    title: str
    author: str
    description: str
    total_copies: int
    # available_copies: int


class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    description: Optional[str] = None
    total_copies: Optional[int] = None
    available_copies: Optional[int] = None
    created_at: Optional[datetime] = None


#Response Schema
class BookOut(BaseModel):
    id: int
    title: str
    author: str
    description: str
    total_copies: int
    available_copies: int
    created_at: datetime

    class Config:
        from_attributes = True


class RentalCreate(BaseModel):
    id: int
    book_id: int
    user_id: int


class RentalOut(BaseModel):
    id: int
    book_id: int
    user_id: int
    rented_at: datetime
    returned_at: Optional[datetime] = None

    class Config:
        from_attributes = True


#token schema
class Token(BaseModel):
    access_token: str
    token_type: str


#schema for token data
class TokenData(BaseModel):
    id: Optional[str] = None 