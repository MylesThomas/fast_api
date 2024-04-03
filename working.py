# working.py
from typing import Annotated, Optional

from fastapi import FastAPI, Path, Query, HTTPException, status

from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    brand: Optional[str] = None

class UpdateItem(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    brand: Optional[str] = None

inventory = {}

@app.get("/get-item/{item_id}")
def get_item(
    item_id: Annotated[int, Path(description="The ID of the item you would like to view.", ge=1)]
):
    if item_id not in inventory:
        raise HTTPException(status_code=404, detail="Item ID does not exist.")
    return inventory[item_id]

@app.get("/get-by-name/{item_id}")
def get_item(
    *,
    item_id: int, # not necessary,
    name: Annotated[str, Query(title="Name", description="Name of item.")],
    # name: Optional[str] = None,
    test: int # not necessary
):
    for item_id in inventory:
        # if inventory[item_id]["name"] == name:
        if inventory[item_id].name == name: # had to update this when we started using BaseModel ie. item
            return inventory[item_id]
    raise HTTPException(status_code=404, detail="Item name does not exist.")

@app.post("/create-item/{item_id}")
def create_item(item_id: int, item: Item):
    if item_id in inventory:
        raise HTTPException(status_code=400, detail="Item ID already exists.")
    
    #inventory[item_id] = {"name": item.name, "price": item.price, "brand": item.brand} (old way)
    inventory[item_id] = item
    return inventory[item_id]

@app.put("/update-item/{item_id}")
def update_item(item_id: int, item: UpdateItem):
    if item_id not in inventory:
        raise HTTPException(status_code=404, detail="Item ID does not exist.")
    
    #inventory[item_id].update(item) [cannot use .update() with BaseModel Class]
    
    # attributes_list = dir(item)
    # attributes_list = [a for a in attributes_list if not a.startswith('__')]
    # print(f"attributes_list for UpdateItem class: {attributes_list}")
    # print(f"inventory[item_id]: {inventory[item_id]}")
    # print(f"item.__class_vars__: {item.__class_vars__}")
    print("3 ways to look at this item that was just submitted via request body:")
    print(item)
    print(item.model_dump())
    print(item.model_dump_json())
    
    hashmap_item_data = item.model_dump(exclude_defaults=True)
    print(f"new item (UpdateItem class): {hashmap_item_data}")
    # for key in hashmap_item_data:
    #     print(f"key: {key}")
    #     key = str(key)
    #     print(f"str(key): {key}")
        
    #     value = hashmap_item_data[key]
    #     if value is not None:
    #         print(f"inventory before: {inventory}")
    #         print(f"for key/variable of {key}, replacing value of {inventory[item_id]} with {value}")
            
    #         print(f"current item_id dict before: {inventory[item_id].__dict__}")
    #         inventory[item_id].__dict__.update({key: value})
            
    #         print(f"current item_id dict after: {inventory[item_id].__dict__}")
    #         print(f"inventory after: {inventory}")
    
    # Update the database (inventory[item_id]) with the request body (item: UpdateItem)
    print(f"before update (item_id={item_id}): {inventory[item_id]}")
    inventory[item_id].__dict__.update(hashmap_item_data)
    print(f"after update (item_id={item_id}): {inventory[item_id]}")
    return inventory[item_id]

@app.delete("/delete-item")
def delete_item(item_id: int = Query(..., description="The ID of the item we are going to delete.", ge=0)):
    if item_id not in inventory:
        raise HTTPException(status_code=404, detail="Item ID does not exist.")
        
    del inventory[item_id]
    return {"Success": f"Item {item_id} deleted!"}