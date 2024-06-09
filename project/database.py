from sqlalchemy import QueuePool, create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, Session, declarative_base

from project.config import settings

# https://fastapi.tiangolo.com/tutorial/sql-databases/#create-the-sqlalchemy-engine
engine = create_engine(
    settings.DATABASE_URL,
    poolclass=QueuePool,
    pool_size=40,
    max_overflow=5,
    pool_timeout=30,
    pool_recycle=3600,
    echo=True
)


def get_session() -> Session:
    session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    custom_scoped_session = scoped_session(session_local)
    return custom_scoped_session()


Base = declarative_base()
