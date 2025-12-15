#NOTE: http://127.0.0.1:8000/predict
'''
a) 127.0.0.1:8000 = street / (server address)

b) /predict = end point of URL so it comes at the end of the url address
            Analogy:
The street /predict has a mailbox (the function). When you “drop a letter” (make a GET request), 
it gives you something back.

c) return = what the server sends back

#NOTE : path operation function : every path requires a function called path operation function.
for eg : home() in the below example 


'''
from pydantic import field_validator
from fastapi.params import Body
from pydantic import BaseModel
from fastapi import FastAPI

app = FastAPI()
#-----------------------------------------------------------------------------------------------

# Decorator makes the below normal function a special path operated function
@app.get("/login")   #NOTE : if i write /logic then it means this will work only when goes on
                    # login section inside the browser
#✅ works = http://127.0.0.1:8001/login
#❌ not work = http://127.0.0.1:8001
def home():
    return {"message": "FastAPI is working!"}


'''
#NOTE : Path parameter : path can have dynamic parts called path parameters. 
@app.get("/predict/{user_id}")
def predict(user_id : int):
    return {"user_id": user_id "}


    /predict/42 → You go to house number 42 on the Predict street.
Every house number can be different, so the function knows which one you meant.
'''

'''
#NOTE : Query paramter : sometimes we don't need dynamic path and we only wnat to send some
        extra data at that time we use query parameters. It just store parameter arguments.
        
        @app.get("/predict")
def predict(user_id: int, feature: int):
    return {"user_id": user_id, "feature": feature}

        #NOTE : we can also use (path + Query parameter together)

    @app.get("/predict/{user_id}")          -- here we are using both together 
def predict(user_id: int, feature: int):
    return {"user_id": user_id, "feature": feature}

        
'''

#NOTE : using another function for different feature than above function
'''
let us say i want to retrieve post posted by users then i will use (get method)
'''
#-----------------------------------------------------------------------------------------------

@app.get("/create_posts")
def post():
    return{"Users_post":"This is the post of users"}

#NOTE: 

#-----------------------------------------------------------------------------------------------

@app.post("/create_accounts")
def reel(acc_data: dict = Body(...)):
    print(f"Server Response : \n{acc_data}")
    return{"acc_data":f"Account successufully created with name: {acc_data['full_name']}"}

'''
#NOTE OUTPUT IN POSTMAN
#  {
    "acc_data": "Account successufully created with name: Rajiv Chaudhary"
}
'''
#-----------------------------------------------------------------------------------------------
# Now creating a model for posting timelines(2,3 lines of description) -- Using normal validation

class Timeline_Node(BaseModel):
    Text : str

@app.post("/validate_Timeline")
def validate_text(content: Timeline_Node):
    # if(type(content) == str): ------- 
    ''' 
    👉 content is never a string.
FastAPI always converts JSON → Pydantic model.
So content is always a Timeline_Node object.
    '''
    return{f"Your timeline is : {content.Text}"}
    # raise ValueError("Timeline must be in string\n")
#-----------------------------------------------------------------------------------------------

#NOTE : a simple model called (girlfriend) to purpose people 

'''
class girlfriend(BaseModel):
    name : str
    status : str
    msg : str

@app.post("/chatWithGirl")
def chat(data: girlfriend):
    if(data.status.lower() == 'single'):
        print(f"{data.name} Since you are {data.status}.So, i have a msg for you but you are only allowed to read after i leave.")
        print("Opening letter .....\n")
        print(f"I {data.msg} you {data.name}")
    return {"Server : "f"Congratulations 🎉 {data.name}"}
'''

#-----------------------------------------------------------------------------------------------
#NOTE : a simple model called (girlfriend) to purpose peple (using custom validation)
'''
Why value doesn’t explicitly mention a class
In a Pydantic field validator, the value parameter is automatically provided by Pydantic.
You don’t have to fetch it from the class manually.
Pydantic inspects the field being validated and passes its current value to the value parameter when creating
the model.

Think of it like a magic hook: Pydantic says:
“Okay, we are creating TimelineNode. Field Text has the value 'Hello'. I know there’s a validator check_text_length for Text, so I’ll call check_text_length(cls, value='Hello') automatically.”
'''

import random
from fastapi import FastAPI
from pydantic import BaseModel, field_validator

app = FastAPI()

class Girlfriend(BaseModel):
    name: str
    status: str
    

    @field_validator("name")
    def check_name(cls, value):
        if not value[0].isupper():
            raise ValueError("First letter of name must be capital")
        else:
            print(f"Name is stored")
        return value

    @field_validator("status")
    def check_status(cls, value):
        if value.lower() not in ["single", "married"]:
            raise ValueError("Status must be either 'single' or 'married'")
        else:
            print(f"Status is stored")
        return value


@app.post("/chatWithGirl")
def chat(data: Girlfriend):
    msg = random.choice(['love','hate'])


    if data.status.lower() in ['single' or 'married']:
        print(f"{data.name}, since you are {data.status}, I have a message for you...")
        print(f"I {msg} you, {data.name}")

    return {"Server": f"Congratulations 🎉 {data.name}"}
