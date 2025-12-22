'''
✅ What we do here

a) Define input data structure
b) Validate incoming JSON
c) Shape API responses
'''
from typing import Optional
from pydantic import BaseModel
from datetime import datetime   #NOTE: in schemas.py datatime.datetime is accepted but in 
#model it doesn;t support 

#NOTE : pydantic for creating a new student
class CreateStudent(BaseModel):     #CreateStudent is used for API responses 
    id: Optional[int] = None      
    name : str
    email : str
    age : int
    course : str
    marks : float
    created_at : Optional[datetime] = None

    model_config = {
        "from_attributes": True
    }
    