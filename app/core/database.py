from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import AsyncGenerator
from app.core.config import settings  

DATABASE_URL = f"postgresql+asyncpg://{settings.USER_DB}:{settings.USER_PASSWORD}@{settings.HOST_DB}:{settings.PORT_DB}/{settings.NAME_DB}"

# Create the database engine and session
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

# Defines a base class for all ORM models. 
Base = declarative_base()

# Obtein the session db 
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
