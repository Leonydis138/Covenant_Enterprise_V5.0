"""Database session management"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import text

from covenant.utils.config import settings

# Create async engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_size=settings.DATABASE_POOL_SIZE,
    max_overflow=40
)

# Session factory
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# Base class for models
Base = declarative_base()

async def init_db():
    """Initialize database"""
    async with engine.begin() as conn:
        await conn.execute(text("SELECT 1"))
        # In production: await conn.run_sync(Base.metadata.create_all)

async def get_db():
    """Dependency for getting DB session"""
    async with async_session() as session:
        yield session