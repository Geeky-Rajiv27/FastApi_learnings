from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from SMS_database import Base, engine, SessionLocal
from SMS_models import student
from SMS_schemas import CreateStudent
from typing import List


app = FastAPI()

#---------------------------------------------------------------------------------
#               CORS SETUP --  CORS setup and endpoint handling in your main.py so your
#                                    frontend can talk to FastAPI properly.
#---------------------------------------------------------------------------------

from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://127.0.0.1:5500",  # your frontend URL (or "*" to allow all)
    "http://localhost:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # or ["*"] to allow all
    allow_credentials=True,
    allow_methods=["*"],    # allow GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],
)

#---------------------------------------------------------------------------------


#NOTE : Creating tables in DB if not exists
Base.metadata.create_all(bind=engine)

#---------------------------------------------------------------------------------
#NOTE : This section is for if i want to give student details via postman as a body raw request               
#---------------------------------------------------------------------------------

#NOTE : database dependencies
def get_db():   #NOTE: Fastapi calls these dependency functions per every HTTP requests
    db = SessionLocal()
    try :
        yield db    #This sends the database session
    finally:
        db.close()  #closing database after each request

#---------------------------------------------------------------------------------
@app.get("/test/")
def test_route():
    return {"message": "Server is running!"}


#---------------------------------------------------------------------------------
# NOTE :        Get all students details from database          
#.all() -> returns list of rows     .first() -> returns first row or None
#---------------------------------------------------------------------------------
#NOTE: ✅ FastAPI automatically converts ORM → dict → JSON  using response_model
@app.get("/AllStudents/")   
def AllStudent(db: Session = Depends(get_db)):
        fetched_Data = db.query(student).all()  #NOTE : student is SQLalchemy modal class name not table name 
        return {
            "message" : "Details of all student are : ",
            "Data" :  fetched_Data
        }


#---------------------------------------------------------------------------------
#NOTE: endpoint for creating a student and posting 
#---------------------------------------------------------------------------------

@app.post("/NewStudent/", response_model=CreateStudent)
def create_student(std: CreateStudent, db: Session = Depends(get_db)):

    created_std = student(
        name = std.name,
        email = std.email,
        age = std.age,
        course = std.course,
        marks = std.marks
      #  created_at = std.created_at    #NOTE : created_at is usually auto-generated in the
      #  database (server_default=func.now()). Don’t pass it manually.
    )

    db.add(created_std)     # Stage the object for insertion
    db.commit()             # Save changes to the database
    db.refresh(created_std) # Refresh to get auto-generated fields like id and created_at
    return created_std      # Return the inserted record as JSON


#---------------------------------------------------------------------------------
#NOTE : Get Specific student data from database using {id}
#---------------------------------------------------------------------------------

@app.get("/students/{std_id}")
def getWithID(std_id: int, db: Session = Depends(get_db)):
     singleStudent = db.query(student).filter(student.id == std_id).first()
     if not singleStudent: #if database sents None (student not found)
          raise HTTPException(status_code=404, detail=f"Student with id {std_id} not found")
     return {
          "message": f"Details of student with id: {std_id}",
          "Details": singleStudent
     }
     

#---------------------------------------------------------------------------------
#NOTE: Update detail of specific student stored in database with {id}
#---------------------------------------------------------------------------------
@app.put("/UpdateStudent/{std_id}")
def UpdateStudentDetails(std_id: int, new_data:CreateStudent ,db: Session = Depends(get_db)):
     fetched_std = db.query(student).filter(student.id == std_id).first()
     if not fetched_std:
         raise HTTPException(status_code=404, detail=f"Student with id {std_id} not found")
     fetched_std.name = new_data.name
     fetched_std.email = new_data.email
     fetched_std.age = new_data.age
     fetched_std.course = new_data.course
     fetched_std.marks = new_data.marks
     db.commit()        #NOTE: saving the new data in the database
     db.refresh(fetched_std)  
     return f"Details of student with id: {std_id} is successfully updated."


#---------------------------------------------------------------------------------
#NOTE: Delete detail of specific student stored in database with {id}
#---------------------------------------------------------------------------------
@app.delete("/DeleteStudent/{std_id}")
def DeleteStudent(std_id: int, db: Session = Depends(get_db)):
     fetched_std = db.query(student).filter(student.id == std_id).first()
     if not fetched_std:
         raise HTTPException(status_code=404, detail=f"Student with id {std_id} not found")
     db.delete(fetched_std)
     db.commit()    #saving the new database that is without deleted one
     #db.refresh(fetched_std)     #Let's python object get the latest changes from the database
#NOTE: db.refresh() is not required since the object is already gone cause
     return {"message" : f"Student with id {std_id} is successfully deleted from database."}