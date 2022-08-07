from starlette import status
from starlette.exceptions import HTTPException
from starlette.responses import Response
from sqlalchemy.orm import Session
from .. import database, schemas, models, oauth2

from fastapi import Depends, APIRouter

import sys

sys.path.append("..")

router = APIRouter(
    tags=['nutrition']
)


@router.get('/meals')
def get_meal(db: Session = Depends(database.get_db)):
    meals = db.query(models.Nutrition).all()

    return meals


@router.post('/meals', response_model=schemas.NutritionResponse)
def create_meal(meal: schemas.Nutrition, db: Session = Depends(database.get_db),
                user_id: int = Depends(oauth2.get_current_user)):
    print(user_id)
    new_meal = models.Nutrition(owner_id=user_id.id, **meal.dict())
    db.add(new_meal)
    db.commit()
    db.refresh(new_meal)

    return new_meal


@router.get('/meals/{id}')
def get_single_meal(id: int, response: Response, db: Session = Depends(database.get_db)):
    meal = db.query(models.Nutrition).filter(models.Nutrition.id == id).first()
    if not meal:
        response.status_code = status.HTTP_404_NOT_FOUND

    return meal


@router.delete('/meals/{id}')
def delete_meal_by_id(id: int, db: Session = Depends(database.get_db),
                      current_user: int = Depends(oauth2.get_current_user)):

    print(current_user)
    meal_query = db.query(models.Nutrition).filter(models.Nutrition.id == id)

    meal = meal_query.first()

    if meal is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="meal not found")

    meal_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/meals/{id}')
def update_meal_by_id(id: int, updated_meal: schemas.Nutrition,
                      db: Session = Depends(database.get_db),
                      user_id: int = Depends(oauth2.get_current_user)):
    print(user_id)
    meal_query = db.query(models.Nutrition).filter(models.Nutrition.id == id)
    meal = meal_query.first()

    if meal is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    meal_query.update(updated_meal.dict(), synchronize_session=False)
    db.commit()

    return meal_query.first()
