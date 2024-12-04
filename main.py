
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import uvicorn

from database import init_db, engine, SessionLocal
import models, schemas, crud

# TODO
# ...

app = FastAPI()

# Создание базы данных.
models.Base.metadata.create_all(bind=engine)

# Зависимость для работы с базой данных.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Эндпоинт добавления пользователя.
@app.post("/add_user/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.login == user.login).first():
        raise HTTPException(status_code=400, detail="Такой логин уже существует.")
    db_user = crud.create_user(db=db, user=user)
    return schemas.UserResponse(login=db_user.login, name=db_user.name)

# Эндпоинт изменения данных пользователя.
@app.put("/user/{user_id}", response_model=schemas.UserResponse)
def update_user(user_id: int, user_update: schemas.UserUpdate, db: Session = Depends(get_db)):
    user = crud.update_user(db=db, user_id=user_id, user_update=user_update)
    if user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден.")
    return user

# Эндпоинт удаления пользователя.
@app.delete("/user/{user_id}/")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.delete_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден.")

# Эндпоинт добавления фильма.
@app.post("/add_movie/", response_model=schemas.MovieResponse)
def create_movie(movie: schemas.MovieCreate, db: Session = Depends(get_db)):
    db_movie = crud.create_movie(db=db, movie=movie)
    return schemas.MovieResponse(title=db_movie.title)

# Эндпоинт изменения данных о фильме.
@app.put("/movie/{movie_id}/", response_model=schemas.MovieUpdate)
def update_movie(movie_id: int, movie: schemas.MovieUpdate, db: Session = Depends(get_db)):
    db_movie = crud.update_movie(db=db, movie_id=movie_id, movie_update=movie)
    if db_movie is None:
        raise HTTPException(status_code=404, detail="Фильм не найден.")
    return db_movie

# Эндпоинт удаления фильма.
@app.delete("/movie/{movie_id}/")
def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    db_movie = crud.delete_movie(db=db, movie_id=movie_id)
    if db_movie is None:
        raise HTTPException(status_code=404, detail="Фильм не найден.")

# Эндпоинт добавления фильма в избранное.
@app.post("/add_favorites/", response_model=schemas.FavoriteBase)
def add_to_favorites(favorite: schemas.FavoriteBase, db: Session = Depends(get_db)):
    if not db.query(models.User).filter(models.User.id == favorite.user_id).first():
        raise HTTPException(status_code=400, detail="Такого пользователя не существует.")
    if not db.query(models.User).filter(models.Movie.id == favorite.movie_id).first():
        raise HTTPException(status_code=400, detail="Такого фильма не существует.")
    return crud.add_to_favorite(db=db, favorite=favorite)

# Эндпоинт удаления фильма из избранного.
@app.delete("/favorite/", response_model=schemas.FavoriteBase)
def remove_from_favorites(favorite: schemas.FavoriteBase, db: Session = Depends(get_db)):
    db_favorite = crud.remove_from_favorite(db=db, favorite=favorite)
    if db_favorite is None:
        raise HTTPException(status_code=404, detail="Список избранного или пользователь не найден.")

# Эндпоинт получения фильмов из избранного.
@app.get("/favorites/{user_id}/")
def get_favorites(user_id: int, db: Session = Depends(get_db)):
    favorites = crud.get_favorites(db=db, user_id=user_id)
    return [{"movie_id": favorite.movie_id,
             "movie": db.query(models.Movie).filter(models.Movie.id == favorite.movie_id).
             first()} for favorite in favorites]


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
