
from pydantic import BaseModel
from typing import List, Optional


# При создании пользователя необходим логин, пароль и имя.
class UserCreate(BaseModel):
    login: str
    password: str
    name: str

# Модель для ответа при создании пользователя.
class UserResponse(BaseModel):
    login: str
    name: str

# При изменении пользователя логин изменить нельзя, только пароль и имя.
class UserUpdate(BaseModel):
    password: str
    name: str

# Модель создания фильма.
class MovieCreate(BaseModel):
    title: str
    rating: Optional[int]
    description: Optional[str]

# Модель для ответа при создании фильма.
class MovieResponse(BaseModel):
    title: str

# Модель для обновления фильма.
class MovieUpdate(BaseModel):
    title: str
    rating: Optional[int]
    description: Optional[str]

# Модель для избранного.
class FavoriteBase(BaseModel):
    user_id: int
    movie_id: int
