from typing import List

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.future import select
from sqlalchemy import update
from sqlmodel import Session

import schemas
import models
from database import engine, my_fast_session, Base, get_async_session
from contextlib import asynccontextmanager
from sqlalchemy import MetaData

metadata = MetaData()


# Dependency
async def get_session():
    db = my_fast_session()
    try:
        yield db
    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI, session: Session = Depends(get_async_session)):
    """
    Функция определяет поведение приложения перед запуском до начала приема запросов и при завершении
    """
    # startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # shutdown
    # await session.close()
    await engine.dispose()


app = FastAPI(lifespan=lifespan)


@app.post('/recipe/', response_model=schemas.RecipeOut)
async def recipe(recipe: schemas.RecipeIn, session: Session = Depends(get_async_session)) -> models.Recipe:
    """
    Функция позволяет добавить рецепт в базу данных, входные параметры задаются схемой
    param recipe: объект схемы RecipeIn представляющий сведения о добавляемом рецепте
    return: возвращает объект модели Recipe
    """
    new_recipe = models.Recipe(**recipe.dict())
    async with session.begin():
        session.add(new_recipe)
    return new_recipe


@app.get('/recipe/')
async def get_all_recipe(session: Session = Depends(get_async_session)) -> List[models.Recipe]:
    """
    Функция позволяет получить перечень всех рецептов в базе данных, а именно их идентификационные номера и названия
    return: возвращает список объектов схемы RecipeAll
    """
    res = await session.execute(select(models.Recipe))
    return res.scalars().all()


@app.get('/recipe/{recipe_id}', response_model=schemas.RecipeOut)
async def get_recipe(recipe_id: int, session: Session = Depends(get_async_session)) -> models.Recipe:
    """
    Функция позволяет выбрать подробную информацию о рецепте из базы данных,
    а также увеличивает счетчик просмотров рецепта
    param recipe_id: идентификатор рецепта в базе данных
    return: возвращает объект схемы RecipeOut
    """
    # async with my_fast_session.begin():
    smtp = (update(models.Recipe).where(models.Recipe.id == recipe_id
                                        ).values(views=models.Recipe.views + 1))
    if smtp is None:
        raise HTTPException(status_code=404, detail="Item not found")
    await session.execute(smtp)
    await session.commit()
    async with session.begin():
        recipe = await session.get(models.Recipe, recipe_id)
        return recipe
