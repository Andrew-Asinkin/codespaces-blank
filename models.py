from sqlalchemy import Column, Integer, String

from database import Base


class Recipe(Base):
    __tablename__ = "Recipes"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    views = Column(Integer, index=True)
    time = Column(Integer, index=True)
