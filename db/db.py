from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import DB_URL

engine = create_engine(url=DB_URL)
session = sessionmaker(bind=engine, expire_on_commit=False)

Base = declarative_base()
Base.metadata.create_all(bind=engine)


def get_db():
    db = session()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
