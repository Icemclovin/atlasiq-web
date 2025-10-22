"""
Database connection and session management
Async SQLAlchemy setup with connection pooling
"""
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import NullPool, QueuePool

from app.config import settings

# Create async engine with connection pooling
# SQLite must use NullPool or StaticPool for async
database_url = settings.get_database_url()
is_sqlite = database_url.startswith("sqlite")

if is_sqlite or settings.DEBUG:
    # SQLite or debug mode: use NullPool
    engine = create_async_engine(
        database_url,
        echo=settings.DB_ECHO,
        poolclass=NullPool,
        connect_args={"check_same_thread": False} if is_sqlite else {},
    )
else:
    # PostgreSQL in production: use QueuePool with pooling
    engine = create_async_engine(
        database_url,
        echo=settings.DB_ECHO,
        pool_pre_ping=True,
        pool_size=settings.DB_POOL_SIZE,
        max_overflow=settings.DB_MAX_OVERFLOW,
        poolclass=QueuePool,
    )

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# Create declarative base for models
Base = declarative_base()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency for FastAPI endpoints to get database session
    
    Usage:
        @router.get("/items")
        async def get_items(db: AsyncSession = Depends(get_db)):
            ...
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db() -> None:
    """
    Initialize database - create all tables
    Should be called on application startup
    """
    async with engine.begin() as conn:
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)


async def close_db() -> None:
    """
    Close database connections
    Should be called on application shutdown
    """
    await engine.dispose()


# Health check function
async def check_db_connection() -> bool:
    """
    Check if database connection is healthy
    Returns True if connection is successful, False otherwise
    """
    try:
        async with engine.connect() as conn:
            from sqlalchemy import text
            await conn.execute(text("SELECT 1"))
        return True
    except Exception as e:
        print(f"Database health check failed: {e}")
        return False
