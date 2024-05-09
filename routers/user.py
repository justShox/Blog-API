from fastapi import HTTPException, status, Depends, APIRouter
from schemas import *
from typing import List
from utils import *
from database import get_db
from sqlalchemy.orm import Session
import models

router = APIRouter(
    prefix='/users',
    tags=['Users']
)


@router.post('/create', status_code=status.HTTP_201_CREATED, response_model=GetUser)
async def create_user(user: CreateUser, db: Session = Depends(get_db)):
    hashed_password = hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/get-all', response_model=List[GetUser])
async def get_all_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


@router.delete('/delete/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: int, db: Session = Depends(get_db)):
    check = db.query(models.User).filter(models.User.id == id)
    if check.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id {id} was not found')
    check.delete(synchronize_session=False)
    db.commit()
