from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.seed_data import DOCTOR_SEED_DATA
from secretsmanager import get_database_url


class Base(DeclarativeBase):
    pass


engine: Engine | None = None
SessionLocal = sessionmaker(autoflush=False, autocommit=False, expire_on_commit=False)


def initialize_database() -> None:
    global engine

    if engine is not None:
        engine.dispose()
    engine = create_engine(get_database_url(), pool_pre_ping=True)
    SessionLocal.configure(bind=engine)

    from app.models.doctor import Doctor

    Base.metadata.create_all(bind=engine)
    with SessionLocal() as session:
        if session.query(Doctor).count() == 0:
            session.add_all(Doctor(**record) for record in DOCTOR_SEED_DATA)
            session.commit()


def get_db() -> Generator[Session, None, None]:
    if engine is None:
        initialize_database()
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
