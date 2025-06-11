from typing import Generator
from sqlalchemy.orm import Session
from app.database.connection import SessionLocal

def get_db() -> Generator[Session, None, None]:
    """
    Provides a database session generator.

    This function facilitates the creation and management of a database session
    using the SessionLocal object. It ensures the session is properly closed once
    operations are completed, regardless of whether exceptions occur during the
    lifetime of the session.

    Yields:
        A database session object of type Session for performing database
        operations.

    :return: A generator that yields active database session objects.
    :rtype: Generator[Session, None, None]
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_database_session() -> Session:
    """
    Creates and returns a new database session instance.

    This function is a utility to initialize and return a new database
    session by using the configured `SessionLocal` object. It ensures
    the session creation is simple, encapsulated, and consistent
    throughout the application.

    :return: A new database session instance.
    :rtype: Session
    """
    return SessionLocal()