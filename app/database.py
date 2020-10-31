import pathlib

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Database:

    engine = None
    SessionLocal = None

    def __init__(self, database_uri=None):
        self.database_uri = database_uri
        self.init_db()

    def setup_engine(self, database_uri=None):
        if database_uri is None:
            db_file_path = pathlib.Path(__file__).parent.parent / "fast_delivery.db"
            database_uri = f"sqlite:///{db_file_path}"
        self.engine = create_engine(database_uri, connect_args={"check_same_thread": False})

    def init_db(self):
        self.setup_engine(self.database_uri)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        Base.metadata.create_all(bind=self.engine)



# def setup_engine(database_uri=None):
#     if database_uri is None:
#         db_file_path = pathlib.Path(__file__).parent.parent / "fast_delivery.db"
#         database_uri = f"sqlite:///{db_file_path}"
#     engine = create_engine(database_uri, connect_args={"check_same_thread": False})
#     return engine
#
#
# engine = setup_engine()
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



