from app import database
from fixtures.load_data import load_fixtures
from pathlib import Path

BASE_DIR = Path(__file__).parent
session = database.SessionLocal()

load_fixtures(session)