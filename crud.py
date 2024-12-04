
from sqlalchemy.orm import Session
from passlib.context import CryptContext

import models, schemas, database


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Создание хеша пароля.
def get_password_hash(password):
    return pwd_context.hash(password)

# Создание пользователя.
def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(login=user.login, hashed_password=hashed_password, name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Изменение данных пользователя. Имя, пароль.
def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        return None
    db_user.hashed_password = get_password_hash(user_update.password)
    db_user.name = user_update.name
    db.commit()
    db.refresh(db_user)
    return db_user

# Удаление пользователя.
def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is not None:
        db.delete(db_user)
        db.commit()
    return db_user

# Добавление фильма.
def create_movie(db: Session, movie: schemas.MovieCreate):
    db_movie = models.Movie(title=movie.title, rating=movie.rating, description=movie.description)
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie

# Изменение данных о фильме. Название, рейтинг, описание.
def update_movie(db: Session, movie_id: int, movie_update: schemas.MovieUpdate):
    db_movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if db_movie is None:
        return None
    # Отбросим значение по умолчанию для FastAPI docs
    if movie_update.title != "string":
        db_movie.title = movie_update.title
    if movie_update.rating != 0:  # ?
        db_movie.rating = movie_update.rating
    if movie_update.description != "string":
        db_movie.description = movie_update.description
    db.commit()
    db.refresh(db_movie)
    return db_movie

# Удаление фильма.
def delete_movie(db: Session, movie_id: int):
    db_movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if db_movie is not None:
        db.delete(db_movie)
        db.commit()
    return db_movie

# Добавление фильма в избранное для пользователя.
def add_to_favorite(db: Session, favorite: schemas.FavoriteBase):
    db_favorite = models.Favorite(user_id=favorite.user_id, movie_id=favorite.movie_id)
    db.add(db_favorite)
    db.commit()
    db.refresh(db_favorite)
    return db_favorite

# Удаление фильма из избранного для пользователя.
def remove_from_favorite(db: Session, favorite: schemas.FavoriteBase):
    db_favorite = db.query(models.Favorite).filter(
        models.Favorite.user_id == favorite.user_id,
        models.Favorite.movie_id == favorite.movie_id
    ).first()
    if db_favorite is not None:
        db.delete(db_favorite)
        db.commit()
    return db_favorite

# Получение фильмов из избранного для выбранного пользователя.
def get_favorites(db: Session, user_id: int):
    return db.query(models.Favorite).filter(models.Favorite.user_id == user_id).all()
