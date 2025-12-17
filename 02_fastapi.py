
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
#-----------------------------------------------------------------------------------------------

#NOTE: function for the post whose id will be given
def find_post(id):
    for p in my_posts:
        if p.get('id') == id:
            return p

#-----------------------------------------------------------------------------------------------
#NOTE : function that will help to find the index of the post from the array
def find_delete_index(id):
    for i,p in enumerate(my_posts):
        if p['id'] == id:
            return i  #This will send the index of the post if post with that specific id exits 
    return None               #otherwise None is sent
#-----------------------------------------------------------------------------------------------

#NOTE : function to find the index of the post that needs to be updated
def find_update_index(id):
    for i ,p in enumerate(my_posts):
        if p['id'] == id:
            return i
    return None
    
#-----------------------------------------------------------------------------------------------

@app.get("/")
def root():
    return {"message": "Hello world"}
#-----------------------------------------------------------------------------------------------

@app.get("/posts")  #NOTE : remember this is /posts with .get
def get_posts():
    return {"data":my_posts}

#-----------------------------------------------------------------------------------------------

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

#-----------------------------------------------------------------------------------------------

#NOTE : to get the post with their id using path parameter {id}
@app.get("/posts/{id}")
def get_post(id: int):

    post = find_post(id)        #NOTE: post <= p        after calling the function from above
    if not post: # if None is sent in case if post with required id is not found  
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND , detail=f"Post with {id} not found")
    return {"post_detial" : post}
#-----------------------------------------------------------------------------------------------
#                                   #NOTE : DELETE
#step 1 : first we have to get the index from users that needs to be deleted.
#step 2 : Then pop the post of that index
#-----------------------------------------------------------------------------------------------
@app.delete("/posts_delete/{id}")
def delete_post(id: int):

    delete_index = find_delete_index(id)
    if delete_index is None: # if delete_index is sent None which is falsy then the condition will be 'true'
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Post with id {id} is not found.")
    my_posts.pop(delete_index)
    return {"Message" : f"Post of id:{id} is sucessfully deleted."}

#-----------------------------------------------------------------------------------------------
#                                   #NOTE : UDPATE
# step 1 : First we have to get the updated post 
# step 2 : Then we have to put that updated post in the existing post that is (my_posts)
# step 3 : To check if post with that specific id exists or not i can use the same index finding
#           function used for delete index finding with different function name
# step 4 : 
#-----------------------------------------------------------------------------------------------

@app.put("/posts/{id}")
def update_Post(id: int, post: Post):

    update_index = find_update_index(id)
    if update_index is None: # if delete_index is sent None which is falsy then the condition will be 'true'
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Post with id {id} is not found.")
    post_dict = post.model_dump()  # passing the post in a python dictionary format
    post_dict['id'] = update_index  # passing update index to the post where we gonna put newOne
    my_posts[update_index] = post_dict      #NOTE : here post_dict is updated post 
    return {"Message" : f"Post of id:{id} is sucessfully updated."}
