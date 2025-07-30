from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession
from sqlalchemy.orm import sessionmaker
from .config import settings
from leodb.models.base import Base

def get_engine() -> AsyncEngine:
    """
    Creates and returns an async SQLAlchemy engine.
    """
    return create_async_engine(
        settings.DATABASE_URL,
        echo=False, # Set to True to log SQL statements
        future=True
    )

def get_session_factory(engine: AsyncEngine) -> sessionmaker:
    """
    Creates and returns a session factory.
    """
    return sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

async def create_database_and_tables(engine: AsyncEngine):
    """
    Creates the database schema and all tables defined in the models.
    """
    async with engine.begin() as conn:
        # You might need to create the schema if it doesn't exist
        # await conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {settings.POSTGRES_SCHEMA}"))
        await conn.run_sync(Base.metadata.create_all)

# Global engine and session factory
engine = get_engine()
SessionFactory = get_session_factory(engine)

async def get_db_session() -> AsyncSession:
    """
    Dependency to get a database session.
    """
    async with SessionFactory() as session:
        yield session