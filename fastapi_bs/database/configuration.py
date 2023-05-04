
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://root:mailong2000@localhost:3306/fastapi' 

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
# , connect_args={"check_same_thread": False}
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()


def get_db():
    """
    Get the database session
    Yields:
        Session: The database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()