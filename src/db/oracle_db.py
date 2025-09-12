import oracledb
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager

from src.db.config import ORACLE_HOST, ORACLE_PORT, ORACLE_USER, ORACLE_PASSWORD, ORACLE_SERVICE, ORACLE_CLIENT

print (f"Oracle Client: {ORACLE_CLIENT}")

if ORACLE_CLIENT:
    oracledb.init_oracle_client(lib_dir=ORACLE_CLIENT)

ORACLE_DATABASE_URL = f"oracle+oracledb://{ORACLE_USER}:{ORACLE_PASSWORD}@{ORACLE_HOST}:{ORACLE_PORT}/?service_name={ORACLE_SERVICE}"

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
