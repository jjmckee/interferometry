from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker
)
from sqlalchemy.orm import (
    declarative_base,
    Session,
    sessionmaker
)

from app.core.config import get_settings


settings = get_settings()

engine = create_engine(settings.DATABASE_URL, echo=False)
session_maker = sessionmaker(autocommit=False, autoflush=False, bind=engine)
async_engine = create_async_engine(settings.ASYNC_DATABASE_URL, echo=False)
async_session_maker = async_sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()


async def get_async_db():
    """
    Asynchronous generator for database session handling.

    Params
    ------
    None
    
    Yields
    -------
    AsyncSession
    """
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()


def get_db() -> Generator[Session, None, None]:
    """
    Generator for database session handling.

    Params
    ------
    None

    Yields
    -------
    Session
    """
    db = session_maker()

    try:
        yield db
    finally:
        db.close()


@contextmanager
def get_db_context() -> Generator[Session, None, None]:
    """
    Context manager for database session handling.

    Params
    ------
    None

    Yields
    -------
    Session
    """
    db_gen = get_db()

    try:
        yield next(db_gen)
    finally:
        try:
            next(db_gen)
        except StopIteration:
            pass