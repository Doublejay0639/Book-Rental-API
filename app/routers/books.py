from fastapi import APIRouter,status, HTTPException, Depends, Response
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



@router.put("/{id}", response_model=schemas.BookOut)
def update_books(id: int, update_book: schemas.BookUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):

    if current_user.role != "owner":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Can't perform that action")
    
    book_query = db.query(models.Book).filter(models.Book.id == id)

    book = book_query.first()

    if book == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} does not exist")
    
    book_query.update(update_book.dict(), synchronize_session=False)

    db.commit()

    return book_query.first()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_books(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):

    if current_user.role != "owner":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Can't perform that action")
    
    book_query = db.query(models.Book).filter(models.Book.id == id)

    book = book_query.first()

    if book == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} does not exist")
    
    rented = db.query(models.Rental).filter(models.Rental.book_id == id, models.Rental.returned_at.is_(None)).first()

    if rented:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Can't delete a rented book")
    

    book_query.delete(synchronize_session=False)

    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
