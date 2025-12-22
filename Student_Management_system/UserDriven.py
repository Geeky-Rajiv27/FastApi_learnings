from SMS_database import SessionLocal
from SMS_main import student
#---------------------------------------------------------------------------------
#NOTE : This is the section for if i want to user giving all details themselves
#---------------------------------------------------------------------------------
def AddStudent():
    db = SessionLocal()
    try:
        name = input("Enter the name of the student : ")
        email = input("Enter the email of the student : ")
        age = int(input("Enter the age of the student : "))
        course = input("Enter the course student likes : ")
        marks = float(input("Enter the marks of the student : "))

    
        new_student = student(
            name=name,
            email=email,
            age=age,
            course=course,
            marks=marks
        )

        db.add(new_student)
        db.commit()
        db.refresh(new_student)
        print(f"Student added with ID: {new_student.id}")
    finally:
        db.close()

AddStudent()