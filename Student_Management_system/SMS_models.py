from sqlalchemy import Column,Integer,String,DateTime,func,Float
from SMS_database import Base

class student(Base):    #NOTE: EntityName = single row of the table (1 student data)
    __tablename__ = "Students_details"  #this is table name that will be shown in mqsql

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    email = Column(String(30), nullable=True, unique=True)
    age = Column(Integer, nullable= False)
    course = Column(String(50), nullable=False)
    marks = Column(Float, nullable=False)
    created_at = Column(DateTime, server_default=func.now()) #NOTE : This uses MySQL’s CURRENT_TIMESTAMP automatically.

