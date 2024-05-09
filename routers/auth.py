from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
import models
from database import get_db
from schemas import UserLogin
from utils import verify_pass
from oauth2 import create_access_token
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(tags=['Authentication'])


@router.post('/login')
async def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.e_mail == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalid credentials')

    if not verify_pass(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid credentials')

    access_token = create_access_token(data={'user_id': user.id})
    return {"Access token": access_token, "token_type": "bearer"}
