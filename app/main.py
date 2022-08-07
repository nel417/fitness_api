from fastapi import FastAPI
from . import models
from .database import engine
from .routers import workout, user, auth

from .config import settings

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(workout.router)
app.include_router(user.router)
app.include_router(auth.router)


