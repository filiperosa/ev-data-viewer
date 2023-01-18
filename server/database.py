from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_PATH = "vehicles_data.db"

DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency for routers
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()