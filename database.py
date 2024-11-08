
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_scoped_session, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from asyncio import current_task
from typing import AsyncGenerator

DATABASE_URL = "sqlite+aiosqlite:///./app.py.db"

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)

session = async_session()
Base = declarative_base()
session_maker = async_sessionmaker(
            engine, autocommit=False, autoflush=False, expire_on_commit=False, class_=AsyncSession
        )
my_fast_session = async_scoped_session(session_maker, scopefunc=current_task)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with my_fast_session() as session:
        yield session
