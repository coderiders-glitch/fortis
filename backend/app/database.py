from collections.abc import Generator

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.secretsmanager import get_database_url


class Base(DeclarativeBase):
    pass


engine: Engine | None = None
SessionLocal: sessionmaker[Session] | None = None


def configure_database() -> None:
    global engine, SessionLocal
    if engine is None:
        engine = create_engine(get_database_url(), pool_pre_ping=True)
        SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db() -> Generator[Session, None, None]:
    configure_database()
    if SessionLocal is None:
        raise RuntimeError("Database session factory is not configured")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
