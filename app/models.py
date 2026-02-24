import enum
from sqlalchemy import Column, Integer, String, text, ForeignKey, Enum
from .database import Base
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship


# class Role(enum.Enum):
#     OWNER = "owner"
#     USER = "user"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False, default="user")
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    rentals = relationship("Rental", back_populates="user")


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    description = Column(String, nullable=False)
    total_copies = Column(Integer, nullable=False)
    available_copies = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    rentals = relationship("Rental", back_populates="book")


class Rental(Base):
    __tablename__ = "rentals"

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id", ondelete="RESTRICT"), nullable=False)
    rented_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))    
    returned_at = Column(TIMESTAMP(timezone=True), nullable=True)

    user = relationship("User", back_populates="rentals")
    book = relationship("Book", back_populates="rentals")