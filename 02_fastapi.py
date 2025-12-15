
from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi import HTTPException, status

global count
count = 0

app = FastAPI()

class Post(BaseModel):
    title : str
    content : str  
    id : Optional[int] = None  #NOTE : since i am generating id automatic via server side so id is optional and None   

my_posts = [        #NOTE : acts as a temporary databse
    {
        "title": "title of post 1",
        "content": "content of post 1",     # NOTE : 1st post 
        "id": 1 
    },
    {
        "title": "title of post 2",
        "content": "content of post 2",     # NOTE : 2nd post
        "id": 2
    },
    {
          "title": "title of post 3",
        "content": "content of post 3",     # NOTE : 3rd post
        "id": 3
    }
]

#NOTE: function for the post whose id will be given
def find_post(id):
    for p in my_posts:
        if p.get('id') == id:
            return p

@app.get("/")
def root():
    return {"message": "Hello world"}

@app.get("/posts")  #NOTE : remember this is /posts with .get
def get_posts():
    return {"data":my_posts}

#NOTE : here in this function if everything worked then it shows 200K oK 
#NOTE : but we can also twick the status code after adding special arguments as below:
from typing import List
@app.post("/posts", status_code = status.HTTP_201_CREATED) #NOTE : remember this is /posts with .post
def create_post(post_carrier: List[Post]):      # NOTE : for List we need to import it 
    created_posts = []  #NOTE : created an empty array

    for post_from_list in post_carrier:
        post_dict = post_from_list.model_dump()       #NOTE: .dict() only works on pydantic v1 (old version)
        post_dict['id'] = count + 1
        count = count + 1
        my_posts.append(post_dict)
        created_posts.append(post_dict)
    
    return {"Post_data ": created_posts}


#NOTE : to get the post with their id using path parameter {id}
@app.get("/posts/{id}")
def get_post(id: int):

    post = find_post(id)        #NOTE: post <= p        after calling the function from above
    if not post: # if None is sent in case if post with required id is not found  
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND , detail=f"Post with {id} not found")
    return {"post_detial" : post}