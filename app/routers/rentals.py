from fastapi import APIRouter,status, HTTPException, Depends
from .. import models, schemas, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime


router = APIRouter(
    prefix="/rentals",
    tags=['Rentals']
)


@router.post("/{id}", response_model=schemas.RentalOut)
def rent_book(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    
    if current_user.role != "user":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Can't perform that action")
    
    book = db.query(models.Book).filter(models.Book.id == id).first()

    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not available")
    
    if book.available_copies <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Out of Stock!")
    
    rented = db.query(models.Rental).filter(models.Rental.user_id == current_user.id, models.Rental.book_id == id, models.Rental.returned_at.is_(None)).first()
    
    if rented:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"You've rented this book before and haven't returned it")

    no_of_rents = db.query(models.Rental).filter(models.Rental.user_id == current_user.id).filter(models.Rental.returned_at.is_(None)).count()

    if no_of_rents >= 3:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Can't have over 3 active rentals")
    
    book.available_copies -= 1

    rental = models.Rental(user_id=current_user.id, book_id=id)

    db.add(rental)
    db.commit()
    db.refresh(rental)
    return rental




@router.get("/me", response_model=List[schemas.RentalOut])
def view_my_rentals(db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):

    if current_user.role != "user":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Can't perform that action")
    
    my_rentals = db.query(models.Rental).filter(models.Rental.user_id == current_user.id).all()

    return my_rentals


@router.get("/", response_model=List[schemas.RentalOut])
def view_all_rentals(db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):

    if current_user.role == "user":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Can't perform that action")
    
    all_rentals = db.query(models.Rental).all()

    if all_rentals == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No rentals to show")

    return all_rentals


@router.put("/return/{id}", response_model=schemas.BookOut)
def return_book(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):

    if current_user.role != "user":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Can't perform that action")
    
    rented_book = db.query(models.Rental).filter(models.Rental.user_id == current_user.id, models.Rental.book_id == id, models.Rental.returned_at.is_(None)).first()

    if not rented_book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No active rental found")

    book = db.query(models.Book).filter(models.Book.id == id).first()

    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="book not found")

    rented_book.returned_at = datetime.utcnow()

    book.available_copies += 1
        
    db.commit()
    # db.refresh(rented_book)
    # db.refresh(book)

    return book