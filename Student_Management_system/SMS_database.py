from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Database_URL = "mysql+pymysql://root:rajiv123@localhost:3306/StudentBase"   #NOTE: DB name = StudentBase
engine = create_engine(Database_URL)
SessionLocal = sessionmaker(
    autocommit = False,
    autoflush= False,
    bind = engine
)

Base = declarative_base()