"""coding=utf-8."""
 
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
 
DATABASE_URL = "postgresql://postgres:123456@127.0.0.1:5432/biblio_test"
 
engine = create_engine(
    DATABASE_URL
)
 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
 
Base = declarative_base()