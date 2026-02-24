from fastapi import APIRouter,status, HTTPException, Depends
from .. import models, schemas, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List, Optional


router = APIRouter(
    prefix="/books",
    tags=['Books']
)


@router.post("/", response_model=schemas.BookOut)
def add_book(Book: schemas.BookCreate, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):

    if current_user.role != "owner":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Can't perform that action")
    
    # book_data = Book.dict()
    # book_data["available_copies"] = book_data["total_copies"]

    book_data = {
        **Book.dict(),
        "available_copies": Book.total_copies
    }

    new_book = models.Book(**book_data)
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

@router.get("/", response_model=List[schemas.BookOut])
def get_all_books(db: Session = Depends(get_db), search: Optional[str] = ""):

    books = db.query(models.Book).filter(models.Book.title.contains(search)).all()
    return books



#Get book by {id} skipped

