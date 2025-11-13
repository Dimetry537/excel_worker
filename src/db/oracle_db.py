import oracledb
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager

from src.db.config import settings

print (f"Oracle Client: {settings.oracle_client}")

if settings.oracle_client:
    oracledb.init_oracle_client(lib_dir=settings.oracle_client)

ORACLE_DATABASE_URL = f"oracle+oracledb://{settings.oracle_user}:{settings.oracle_password}@{settings.oracle_host}:{settings.oracle_port}/?service_name={settings.oracle_service}"

engine = create_engine(
    ORACLE_DATABASE_URL,
    echo=True,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    class_=Session
)

@contextmanager
def get_db_session():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except:
        db.rollback()
        raise
    finally:
        db.close()

def get_db():
    with get_db_session() as session:
        yield session
