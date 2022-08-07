from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey


class WorkoutBase(Base):
    __tablename__ = "workouts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    reps = Column(Integer, nullable=False)
    notes = Column(String, nullable=True)
    owner_id = Column(Integer, ForeignKey("lifters.id", ondelete="CASCADE"), nullable=False)


class Lifter(Base):
    __tablename__ = "lifters"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)


class Nutrition(Base):
    __tablename__ = "meals"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    meal_number = Column(Integer, nullable=False)
    calories = Column(Integer, nullable=False)
    notes = Column(String, nullable=True)
    owner_id = Column(Integer, ForeignKey("lifters.id", ondelete="CASCADE"), nullable=False)
