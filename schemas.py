from pydantic import BaseModel


class BaseRecipe(BaseModel):
    name: str
    views: int
    time: int


class RecipeAll(BaseModel):
    id: int
    name: str


class RecipeIn(BaseRecipe):
    ...


class RecipeOut(BaseRecipe):
    id: int

    class Config:
        orm_mode = True
