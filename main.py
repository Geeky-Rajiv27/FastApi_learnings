from fastapi import FastAPI, Depends
from database import Base, SessionLocal, engine
from models import students
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List



Base.metadata.create_all(bind=engine)
app = FastAPI()

#NOTE: creating database session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#NOTE : pydantic models for validations
class StudentSchema(BaseModel):
    name : str
    email : str
    model_config = {
        "from_attributes": True
    }

    #NOTE: In V1, orm_mode = True tells Pydantic:   “I will give you SQLAlchemy ORM objects.
    #  Read attributes from them.” #NOTE: this converts dictionary into json

#NOTE : pydantic model 2 
class StudentCreateSchema(StudentSchema):
    password : str
    model_config = {
        "from_attributes": True
    }

#NOTE : THis retrives [] empty json since db is empty
@app.get("/students", response_model=List[StudentSchema])
def get_students(db:Session = Depends(get_db)):
    return db.query(students).all()     #This will retrive all db data


#NOTE :Creating a model to create a document of a student
@app.post("/Createstudents", response_model=StudentCreateSchema)
def create_students(student_Data: StudentCreateSchema, db:Session = Depends(get_db)):
    u=students(
        name=student_Data.name,
        email=student_Data.email,
        password=student_Data.password
        )
    db.add(u)
    db.commit()
    db.refresh(u)
    return u    #NOTE : u is an object that has info of all students 

