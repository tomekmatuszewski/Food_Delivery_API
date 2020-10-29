import pathlib

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Database:

    engine = None
    SessionLocal = None

    def setup_engine(self, database_uri=None):
        if database_uri is None:
            db_file_path = pathlib.Path(__file__).parent.parent / "fastfood.db"
            database_uri = f"sqlite:///{db_file_path}"
        self.engine = create_engine(database_uri, connect_args={"check_same_thread": False})

    def init_db(self, database_uri=None):
        self.setup_engine(database_uri)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        Base.metadata.create_all(bind=self.engine)



# def setup_engine(database_uri=None):
#     if database_uri is None:
#         db_file_path = pathlib.Path(__file__).parent.parent / "fastfood.db"
#         database_uri = f"sqlite:///{db_file_path}"
#     engine = create_engine(database_uri, connect_args={"check_same_thread": False})
#     return engine
#
#
# engine = setup_engine()
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



