"""Database connection and session management for The Great GASPI"""

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session
from geoalchemy2 import Geometry
import logging

from .config import settings

logger = logging.getLogger(__name__)

# Create SQLAlchemy engine
engine = create_engine(
    settings.database_url,
    pool_size=settings.database_pool_size,
    max_overflow=settings.database_max_overflow,
    echo=settings.debug_mode,
)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db() -> Session:
    """Dependency for getting database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database (create tables if they don't exist)"""
    try:
        logger.info("Initializing database schema...")

        # This would normally run migrations
        # In production, use Alembic for schema management
        # For now, manual SQL file execution:
        # psql -U gsapi -d gsapi -f migrations/001_init_schema.sql

        logger.info("Database initialization complete")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise


# PostGIS event listeners
@event.listens_for(engine, "connect")
def receive_connect(dbapi_conn, connection_record):
    """Enable PostGIS extensions on connection"""
    cursor = dbapi_conn.cursor()
    cursor.execute("CREATE EXTENSION IF NOT EXISTS postgis")
    cursor.close()
