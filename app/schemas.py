from pydantic import BaseModel, EmailStr, Field
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
    total_copies: int = Field(gt=0)
    # available_copies: int


class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    description: Optional[str] = None
    total_copies: Optional[int] = Field(None, gt=0)
    available_copies: Optional[int] = Field(None, ge=0)


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


class RentedBook(BaseModel):
    id: int
    title: str
    author: str
    description: str


class RentalOut(BaseModel):
    id: int
    book_id: int
    user_id: int
    rented_at: datetime
    returned_at: Optional[datetime] = None
    user: UserOut
    book: RentedBook

    class Config:
        from_attributes = True


#token schema
class Token(BaseModel):
    access_token: str
    token_type: str


#schema for token data
class TokenData(BaseModel):
    id: Optional[str] = None 