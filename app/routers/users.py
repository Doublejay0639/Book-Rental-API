from fastapi import APIRouter,status, HTTPException, Depends
from .. import models, schemas, utils, database, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List


router = APIRouter(
    prefix="/users",
    tags=['Users']
)


#temporary endpoint to create owner account
@router.post("/", response_model=schemas.UserOut)
def create_owner(owner: schemas.UserCreate, db: Session = Depends(get_db)):

    hashed_password = utils.hash(owner.password)
    owner.password = hashed_password

    new_owner = models.User(**owner.dict())
    db.add(new_owner)
    db.commit()
    db.refresh(new_owner)
    return new_owner



@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserCreate)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/me", response_model=schemas.UserOut)
def view_my_profile(db: Session = Depends(database.get_db), current_user: models.User = Depends(oauth2.get_current_user)):

    # user = db.query(models.User).filter(current_user.id == models.User.id).first()

    # if not user:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Account not found")

    if current_user.role != "user":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Can't view your own profile!!")
    
    return current_user



@router.get("/", response_model=List[schemas.UserOut])
def get_all_users(db: Session = Depends(database.get_db), current_user: models.User = Depends(oauth2.get_current_user)):

    # user = db.query(models.User).filter(current_user.id == models.User.id).first()


    if current_user.role == "user":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Can't perform this action!!")
    

    users = db.query(models.User).all()

    return users


@router.get("/{id}", response_model=schemas.UserOut)
def get_user_by_id(id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(oauth2.get_current_user)):

    if current_user.role == "user":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Can't perform this action!!")
    

    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with {id} not found")
    
    return user