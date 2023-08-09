from dotenv import dotenv_values

from fastapi import HTTPException, status
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.exc import SQLAlchemyError


class Base(DeclarativeBase):
    pass


config = dotenv_values(".env")
SQLALCHEMY_DATABASE_URL = config.get('DATABASE_URL')
SQLALCHEMY_DATABASE_URL = 'postgresql+psycopg2://postgres:567234@195.201.150.230:5433/denis_fill_fa'
engine = create_engine(SQLALCHEMY_DATABASE_URL)
DBSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency
def get_db():
    db = DBSession()
    try:
        yield db
    except SQLAlchemyError as err_sql:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err_sql))
    finally:
        db.close()
