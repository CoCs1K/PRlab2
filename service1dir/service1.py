from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    name: str
    age: int

users_db = {}
user_id_counter = 1

@app.get("/users/{user_id}")
def get_user(user_id: int):
    print(users_db)
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    return users_db[user_id]

@app.post("/users")
def create_user(user: User):
    global user_id_counter
    users_db[user_id_counter] = user
    user_id_counter += 1
    return {"id": user_id_counter - 1, "user": user}

@app.put("/users/{user_id}")
def update_user(user_id: int, user: User):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    users_db[user_id] = user
    return {"id": user_id, "user": user}

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    del users_db[user_id]
    return {"message": "User deleted successfully"}
