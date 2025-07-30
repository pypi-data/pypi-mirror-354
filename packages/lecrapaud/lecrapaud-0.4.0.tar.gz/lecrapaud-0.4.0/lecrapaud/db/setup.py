from sqlalchemy import create_engine, text, MetaData
from sqlalchemy.orm import sessionmaker
import os
from contextlib import contextmanager
from dotenv import load_dotenv

load_dotenv()

if os.getenv("PYTHON_ENV") == "Test":
    DB_USER = os.getenv("TEST_DB_USER", "root")
    DB_PASSWORD = os.getenv("TEST_DB_PASSWORD", "")
    DB_HOST = os.getenv("TEST_DB_HOST", "127.0.0.1")
    DB_PORT = os.getenv("TEST_DB_PORT", "3306")
    DB_NAME = os.getenv("TEST_DB_NAME", "test_stock_db")
else:
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "3306")
    DB_NAME = os.getenv("DB_NAME", "stock_db")

# Step 1: Connect to MySQL without a database
root_engine = create_engine(
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/"
)

# Step 2: Create database if it doesn't exist
with root_engine.connect() as conn:
    conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}"))
    conn.commit()

# Step 3: Connect to the newly created database
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL, echo=False)

# Step 4: Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Step 5: Create tables
RESET_DB = False
if RESET_DB:
    metadata = MetaData()
    metadata.reflect(bind=engine)
    metadata.drop_all(bind=engine)
# Base.metadata.create_all(bind=engine)


# Dependency to get a session instance
@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        db.rollback()
        raise Exception(e)
    finally:
        db.close()
