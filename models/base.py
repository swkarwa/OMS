from contextlib import contextmanager
from pathlib import Path

from sqlalchemy import Engine, create_engine, event
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session


class Base(DeclarativeBase):
    pass


engine = None
SessionLocal = None


def _create_db():
    Base.metadata.create_all(bind=engine)


def _drop_db():
    Base.metadata.drop_all(bind=engine)


def init_db(db_url: str):
    global engine, SessionLocal

    engine = create_engine(db_url, echo=True)

    # ✅ Enable SQLite foreign keys PER CONNECTION
    if db_url.startswith("sqlite"):

        @event.listens_for(Engine, "connect")
        def enable_sqlite_fk(dbapi_connection, connection_record):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()

    SessionLocal = sessionmaker(
        bind=engine,
        autocommit=False,
        autoflush=False,
        expire_on_commit=False,
    )

    _create_db()


def reset_db():
    _drop_db()
    _create_db()


@contextmanager
def get_session():
    """Provide a transactional scope around a series of operations."""
    session: Session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error : {e}")
        raise
    finally:
        session.close()


def get_db():
    """Generator for FastAPI/Flask dependency injection."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
