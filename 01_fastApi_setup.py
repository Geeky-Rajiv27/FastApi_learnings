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


from fastapi import FastAPI

app = FastAPI()

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
@app.get("/create_posts")
def post():
    return{"Users_post":"This is the post of users"}

#NOTE: 
from fastapi.params import Body

@app.post("/create_account")
def reel(acc_data: dict = Body(...)):
    print(f"Server Response : \n{acc_data}")
    return{"acc_data":f"Account successufully created with name: {acc_data['full_name']}"}

'''
#NOTE OUTPUT IN POSTMAN
#  {
    "acc_data": "Account successufully created with name: Rajiv Chaudhary"
}
'''
