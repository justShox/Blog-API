from fastapi import HTTPException, status, Depends, APIRouter

from oauth2 import get_current_user
from schemas import *
from typing import List
from database import get_db
from sqlalchemy.orm import Session
import models

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)


@router.get('/get-all', status_code=status.HTTP_200_OK, response_model=List[PostResponse])
async def get_all_blogs(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@router.post('/create-post', status_code=status.HTTP_201_CREATED, response_model=PostResponse)
async def create_post(post: Post, db: Session = Depends(get_db),
                      current_user: int = Depends(get_current_user)):
    print(current_user.e_mail)
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get('/{id}', status_code=status.HTTP_200_OK)
async def get_post(id: int, db: Session = Depends(get_db),
                   current_user: int = Depends(get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id {id} was not found')
    return post


@router.delete('/delete/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db),
                      current_user: int = Depends(get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id {id} was not found')
    post.delete(synchronize_session=False)
    db.commit()


@router.put('/update/{id}')
async def update_post(id: int, post: UpdatePost, db: Session = Depends(get_db),
                      current_user: int = Depends(get_current_user)):
    check_data = db.query(models.Post).filter(models.Post.id == id)

    if check_data.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id {id} was not found')

    check_data.update(post.dict(), synchronize_session=False)
    db.commit()
    return check_data.first()
