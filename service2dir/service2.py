from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx

app = FastAPI()


class Order(BaseModel):
    user_id: int
    product: str
    quantity: int


orders_db = {}
order_id_counter = 1
USER_SERVICE_URL = "http://service1app:8000/users"


@app.get("/orders/{order_id}")
def get_order(order_id: int):
    if order_id not in orders_db:
        raise HTTPException(status_code=404, detail="Order not found")
    return orders_db[order_id]

@app.post("/orders")
def create_order(order: Order):
    global order_id_counter
    user_response = httpx.get(f"{USER_SERVICE_URL}/{order.user_id}")
    print(user_response)
    if user_response.status_code != 200:
        raise HTTPException(status_code=404, detail="User not found")
    orders_db[order_id_counter] = order
    order_id_counter += 1
    return {"id": order_id_counter - 1, "order": order}

@app.put("/orders/{order_id}")
def update_order(order_id: int, order: Order):
    if order_id not in orders_db:
        raise HTTPException(status_code=404, detail="Order not found")
    orders_db[order_id] = order
    return {"id": order_id, "order": order}

@app.delete("/orders/{order_id}")
def delete_order(order_id: int):
    if order_id not in orders_db:
        raise HTTPException(status_code=404, detail="Order not found")
    del orders_db[order_id]
    return {"message": "Order deleted successfully"}
