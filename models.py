from database import Base
from sqlalchemy import Column, Integer, String

class students(Base):
    __tablename__ = "students"
    id= Column(Integer, primary_key=True, index= True)
    name= Column(String(50))
    email= Column(String(100), unique=True)
    password= Column(String(100))

    #NOTE: Now the above model will be imported on main.py