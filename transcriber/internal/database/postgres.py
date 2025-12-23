from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from configs.config import postgresConfig

database_url = f"postgresql+psycopg://{postgresConfig.POSTGRES_USER}:{postgresConfig.POSTGRES_PASSWORD}@{postgresConfig.POSTGRES_HOST}:{postgresConfig.POSTGRES_PORT}/{postgresConfig.POSTGRES_DB}"
engine = create_engine(database_url, pool_pre_ping=True, future=True)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()