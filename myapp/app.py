from pydantic import BaseModel
# from fastapi.params import Body
# noinspection PyUnresolvedReferences
from fastapi import FastAPI, Response, status, HTTPException
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()


# creating the schema of our API with Pydantic BaseModel
class Post(BaseModel):
    # retrieves post from the frontend and validates it
    title: str
    content: str


try:
    conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres',
                            password='1993200214tonye', cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("database connection was successful")
except Exception as error:
    print("connecting to database failed")
    print("Error:", error)

# variable that stores all of the post(in array) created globally
my_posts = [{"title": "new posts 1", "content": "i love jokes", "id": 1, },
            {"title": "post 2", "content": "content 2", "id": 2}]


# logic for finding a particular post

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p


# logic for deleting post

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i


@app.get("/")
def root():
    return {"message": "hello world"}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(new_post: Post):
    # change "new_post" to a dictionary & assign it to a variable post_dict
    post_dict = new_post.dict()
    # creating a random id for our new_post
    post_dict["id"] = randrange(0, 100000)
    # storing retrieved post from the frontend to my_posts array
    my_posts.append(post_dict)
    # returning the newly created new_post to the frontend
    return {"data": post_dict}


# how to retrieve a particular post
@app.get("/posts/{id}")
def get_one_post(id: int):
    # calling the logic find_post
    post = find_post(id)
    # logic for sending an error message to the frontend
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    return {"new_detail": post}


# how to delete post
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # calling the delete logic
    index = find_index_post(id)

    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} doesn't exist")

    # delete the post from the array my_posts
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# update post

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)

    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} doesn't exist")

    post_dict = post.dict()
    post_dict["id"] = id
    my_posts[index] = post_dict

    return {"data": post_dict}
