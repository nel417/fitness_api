from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import models, utils, oauth2, schemas
from ..database import get_db

router = APIRouter(
    tags=['authentication']
)


@router.post('/login', response_model=schemas.Token)
def login_user(user_creds: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.Lifter).filter(
        models.Lifter.email == user_creds.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"invalid creds")

    if not utils.verify_password(user_creds.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403, detail=f"wrong creds")

    # create token
    access_token = oauth2.create_access_token(
        data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "Bearer"}
