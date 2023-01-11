import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

database_url = os.getenv("DATABASE_URL")
# database_url = "mysql+pymysql://tatenda:tatenda1@127.0.0.1:3306/project"
engine = create_engine(database_url)
SessionLocal = sessionmaker(autocommit=False,
                            autoflush=False,
                            bind=engine)

Base = declarative_base()


def init_db():
    Base.metadata.create_all(bind=engine)


def get_db():
    """
    Establish a connection to the database and maintain the connection in a session object
    """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
