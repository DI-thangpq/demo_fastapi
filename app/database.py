from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

from ssl import create_default_context

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

my_ssl_ctx = create_default_context()

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True,
    connect_args={'ssl': my_ssl_ctx} 
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession
)

Base = declarative_base()

async def get_db():
    async with SessionLocal() as db:
        yield db