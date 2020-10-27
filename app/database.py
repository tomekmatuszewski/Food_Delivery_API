import pathlib

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


def setup_engine(database_uri=None):
    if database_uri is None:
        db_file_path = pathlib.Path(__file__).parent.parent / "fastfood.db"
        database_uri = f"sqlite:///{db_file_path}"
    engine = create_engine(database_uri, connect_args={"check_same_thread": False})
    return engine


engine = setup_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
