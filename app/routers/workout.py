from starlette import status
from starlette.exceptions import HTTPException
from starlette.responses import Response
from sqlalchemy.orm import Session
from .. import database, schemas, models, oauth2

from fastapi import Depends, APIRouter

import sys
sys.path.append("..")

router = APIRouter(
    tags=['workouts']
)


@router.get('/workouts')
def get_workouts(db: Session = Depends(database.get_db)):
    workouts = db.query(models.WorkoutBase).all()

    return workouts


@router.post('/loglift', response_model=schemas.WorkoutResponse)
def create_workout(workout: schemas.Workout, db: Session = Depends(database.get_db),
                   user_id: int = Depends(oauth2.get_current_user)):
    print(user_id)
    new_workout = models.WorkoutBase(owner_id=user_id.id, **workout.dict())
    db.add(new_workout)
    db.commit()
    db.refresh(new_workout)

    return new_workout


@router.get('/workouts/{id}')
def get_single_workout(id: int, response: Response, db: Session = Depends(database.get_db)):
    workout = db.query(models.WorkoutBase).filter(models.WorkoutBase.id == id).first()
    if not workout:
        response.status_code = status.HTTP_404_NOT_FOUND

    return workout


@router.delete('/workouts/{id}')
def delete_workout_by_id(id: int, db: Session = Depends(database.get_db),
                      current_user: int = Depends(oauth2.get_current_user)):

    workout_query = db.query(models.WorkoutBase).filter(models.WorkoutBase.id == id)

    workout = workout_query.first()

    if workout is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="workout not found")

    workout_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/workouts/{id}')
def update_workout_by_id(id: int, updated_workout: schemas.Workout,
                      db: Session = Depends(database.get_db),
                      user_id: int = Depends(oauth2.get_current_user)):
    print(user_id)
    workout_query = db.query(models.WorkoutBase).filter(models.WorkoutBase.id == id)
    workout = workout_query.first()

    if workout is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


    workout_query.update(updated_workout.dict(), synchronize_session=False)
    db.commit()

    return workout_query.first()
