from starlette import status
from starlette.exceptions import HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from .. database import get_db

from fastapi import Depends, APIRouter

"""

Users

"""


router = APIRouter(
    tags=['users']
)


@router.post('/users', status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.Lifter, db: Session = Depends(get_db)):
    hashed_pass = utils.hash(user.password)
    user.password = hashed_pass
    new_user = models.Lifter(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get('/users/{id}',  response_model=schemas.UserResponse)
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    user = db.query(models.Lifter).filter(models.Lifter.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return user
