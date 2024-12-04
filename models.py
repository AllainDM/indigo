
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel

from database import Base

# Таблица с пользователями.
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    login = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    name = Column(String)

    favorites = relationship("Favorite", back_populates="user", cascade="all, delete-orphan")

# Таблица с фильмами.
class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    rating = Column(Integer)
    description = Column(String)

    favorites = relationship("Favorite", back_populates="movie", cascade="all, delete-orphan")

# Таблица с избранным.
class Favorite(Base):
    __tablename__ = "favorites"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    movie_id = Column(Integer, ForeignKey("movies.id", ondelete="CASCADE"), primary_key=True)

    user = relationship("User", back_populates="favorites")
    movie = relationship("Movie", back_populates="favorites")
