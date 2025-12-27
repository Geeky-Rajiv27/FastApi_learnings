'''
✅ What we do here

a) Define input data structure
b) Validate incoming JSON
c) Shape API responses
'''
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# -----------------------------
# Input schema (for POST / PUT)
# -----------------------------
class CreateStudent(BaseModel):
    name: str
    email: str
    age: int
    course: str
    marks: float

# -----------------------------
# Output schema (for responses)
# -----------------------------
class StudentResponse(CreateStudent):       #NOTE:  this class is inheriting from above class
    id: int                         # so , both class will be used according to there use
    created_at: Optional[datetime] = None

    model_config = {
        "from_attributes": True
    }
    