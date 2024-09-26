from contextlib import contextmanager

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from src.models import Base

engine = create_engine('sqlite:///actividad_sospechosa.db')
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
