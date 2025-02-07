# FAST API

---

## Advantages

Very fast
1. Data validation is done for you
- When you create an API, you define types
    - Typically: You don't explicityly set this
        - This means you end up having to do a lot of data validation

2. Auto Documentation
- Since you give the types, it can automatically generate documentation
- Test script

3. Auto Completion and Code Suggestions
- Because you are defining types, 


## Installation

Instructions:
1. Open terminal/command prompt

2. Download FastAPI and uvicorn via pip

```
pip install fastapi uvicorn
```

FastAPI: modern, fast (high-performance), web framework for building APIs with Python
uvicorn: web server implementation for Python

3. Setup project directory and a Python file to work frpom

```
mkdir fast_api
cd fast_api
echo > working.py
```

## Writing our 1st FastAPI

Start with your program:

```py
# working.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"Data": "Test"}
```

What is going on here:
- Importing dependencies:
    - FastAPI: instance of the FastAPI class

- Create an instance of the FastAPI class
    - Initializes our API object
        - We have just created our first FastAPI
        - Must do this whenever you start working with FastAPI

- Create a root/endpoint
    - "slash something" after the main domain
        - Home: just the slash itself
    - Quick description of an endpoint:
        - base server/url: localhost
            - We are not distributing/deploying this app, so running it locally
        - endpoint: hello
            - Different information can be sent/received to/from different endpoints
    - Main types of endpoints:
        - GET: 
        - POST: 
        - PUT: 
        - DELETE: 

## Running our API

Instructions:
1. Make sure you are in the correct working directory

```
cd fast_api
```

2. Run the API using uvicorn

```
uvicorn working:app --reload
```

Note: See how I did not add the `.py` after working

What is going on here:
- uvicorn: server implementation
    - great choice for real-time applications

- working:app
    - name of Python file
    - colon
    - name of variable that FastAPI() is stored under

- --reload: tells uvicorn to constantly reload the web server (everytime you make a change to the Python file that stores the API)

What you should see now:
- "Application startup complete."
- Uvicorn running on http://127.0.0.1:8000

Open this in Google Chrome to see {"Data":"Test"}

Notes:
- http://127.0.0.1:8000 == localhost (basically)
- If you update the Python file and refresh the Google Chrome page, you will see the changes
- If you would like to see the documentation that is automatically generated by FastAPI, head to this page: http://127.0.0.1:8000/docs/
    - You can test out each endpoint via clicking on it -> 'Try it out' -> Execute

## What is an API?

API: Application Programming Interface
- Definition: Web service that provides an interface to applications, to manipulate/retrieve information
- Essentially what it is: 1 backend responsible for distributing all of the data/information for a product/service
- Good practice: separating frontend + backend
    - If you want to create a different representation of the data, you use the same API, just change the way it is displayed!
- Example: Amazon (Has multiple APIs)
    - Inventory API
        - track what is in stock/not in stock
        - Separate from different front ends
        - Multiple inventory APIS
            - Web, Mobile, Alexa, Google Home
                - All rely on the same underlying information
                    - This makes it so that you do not need 5 backends for every application

        - What happens when you search, for example, graphics cards (on any device):
            - Request "Hey I am looking for graphics cards" is made by client (you) and sent to host (Amazon)
            - Response is returned to the front-end, information is displayed on your screen
        - Clicking on a specific graphics card:
            - Request made to get information
            - Response is returned to the front end

## JSON Explanation

JSON: 
- Definition: 
- Essentially what it is: The data APis exchange, anything exchanged over HTTP
- FastAPI: Automatically returns data as JSON (standard format for return calls)
    - "JSONifying our information"
        - so we can work with strictly Python types in our actual API
        - Python dict is standard
            - even if you return something else, it may appear different on the frontend
    
In the following temporary code, we will receive the data on the frontend as JSON:

```py
@app.get("/")
def home():
    return {"Data": "Testing"}
```

Remember this going forward:
- Client/Frontend making request: JSON -> Vanilla Python
    - No need to DE-JSONify, it comes in as a dict

- Host/Backend making response/return calls: Vanilla Python -> JSON
    - FastAPI automatically JSONifies the Vanilla Python for us

## Creating more endpoints + GET Method

New code (temporary):

```py
# working.py
@app.get("/about")
def about():
    return {"Data": "About"}
```

What is going on here:
- another example of a GET Method
    - Client goes to the endpoint to get data, the backend server this simple dictionary of data

Future state: An endpoint serves a webpage, or more interesting data

## Path/Endpoint Parameters

Our first real example: An inventory management system

```py
# working.py
inventory = {
    # id: item
    1: {
        "name": "Milk",
        "price": 3.99,
        "brand": "Regular"
    }

}

@app.get("/get-item/{item_id}")
def get_item(item_id: int):
    return inventory[item_id]
```

What is going on here:
- Inventory
    - In reality: We would be connected to a live database

- Path definition:
    - path: /get-item
    - parameter: {item_id}
        - is inside of curly braces because it is a parameter that could be anything
        - this becomes an argument/parameter
            - it will affect what our backend function returns to the client/frontend user

- Function definition:
    - name: get_item
        - should describe the action

    - parameter: item_id: int
        - parameter: item_id
            - has to match the parameter from the path definition
        - type hint: int
            - tells FastAPI that this item_id parameter is supposed to be an integer
                - if you try to pass something besides an integer, FastAPI will return an error

Let's try test endpoint out by heading to the following link: http://127.0.0.1:8000/get-item/1

We get all of the information needed!

What happens if we do the following:
- get-item/2: Internal Server Error
    - We have not handled errors yet correctly, so we get this vague error

- get-item/"milk":{"detail":[{"type":"int_parsing","loc":["path","item_id"],"msg":"Input should be a valid integer, unable to parse string as an integer","input":"\"milk\"","url":"https://errors.pydantic.dev/2.6/v/int_parsing"}]}
    - FastAPI automatically handles type errors (if you use type hints)

Note: If we want to use multiple path parameters, we could do something like the following:

```py
@app.get("/get-item/{item_id}/{name}")
def get_item(item_id: int, name: str = None):
    return inventory[item_id]
```

Path(): Allows you to add more detail/enforcements on our path parameter
- Example: Adding a description parameter to tell the user what this is

```py
from typing import Annotated

from fastapi import FastAPI, Path

@app.get("/get-item/{item_id}")
def get_item(
    item_id: Annotated[int, Path(description="The ID of the item you would like to view.", ge=1)]
):
    return inventory[item_id]
```

What is going on here:
- Import dependencies
    - Annotated: Special typing form to add context-specific metadata to an annotation
    - Path: You can declare path "parameters" or "variables" with the same syntax used by Python format strings

- Annotated[]: 
    - Support for type hints
    - Arguments:
        - argument 1: type
        - argument 2: Path()

- Path(): 
    - description: description of the the parameter passed (`item_id`)
        - Used to help describe what is going on in your API
            - If you head to http://127.0.0.1:8000/docs, you will now see this description in the docs!

    - Number validation(s): ge=1
        - Used to validate the input
        - examples:
            - gt: greater than
            - lt: less than
            - ge: greater than or equal to
            - le: less than or equal to
            - multiple_of: a multiple of a given number
            - allow_inf_nan: allow 'inf', '-inf', 'nan' values
        - you can pass more than 1 of these at once

    - Not applicable here but good to know:
        - String contraints:
            - min_length
            - max_length
            - pattern: a regular expression that the string must match
        
        - Decimal contraints:
            - max_digits: Maximum number of digits within the Decimal. It does not include a zero before the decimal point or trailing decimal zeroes.
            - decimal_places: Maximum number of decimal places allowed. It does not include trailing decimal zeroes.
        
        - Dataclass contraints:
            - init: Whether the field should be included in the __init__ of the dataclass
            - init_var: Whether the field should be seen as an init-only field in the dataclass
            - kw_only: Whether the field should be a keyword-only argument in the constructor of the dataclass
        
        
        

## Query Parameters

Query Parameters: 
- Allows the client to pass parameters in their request to the API 
- Comes after the ? in a url

Let's look at an example that accepts 1 query parameter:

```py
@app.get("/get-by-name")
def get_item(name: str):
    for item_id in inventory:
        if inventory[item_id]["name"] == name:
            return inventory[item_id]
    return {"Data": "Not found"}
```

What is going on here:
- Path: .get("/get-by-name")
    - notice how there is not curly brackets {}
        - By default: if it does not see the variable described as a parameter in the endpoint's path, it defaults to a query parameter

- Function definition: name: str
    - This allows the function to accept 1 query parameter, which is `name`

Test this function out with the following URL: http://127.0.0.1:8000/get-by-name?name=Milk

What happens if we do the following:
- /get-by-name?name=Milk
    - {"name":"Milk","price":3.99,"brand":"Regular"}

- /get-by-name?name=tim
    - {"Data":"Not found"}

- /get-by-name
    - {"detail":[{"type":"missing","loc":["query","name"],"msg":"Field required","input":null,"url":"https://errors.pydantic.dev/2.6/v/missing"}]}
        - We need to include this parameter, it is required!


Next: How to add more detail to our query parameters (and potentially make them optional!)

```py
from typing import Annotated, Optional

def get_item(name: Optional[str] = None):
```

What is going on here:
- Import dependencies
    - Optional: equivalent to X | None
        - Allows explicit use of `None` to be allowed
            - Note: Not the same as an optional argument ie. one that has a default

- Optional[str]: makes the passing of a string `name` optional
    - Method recommended by FastAPI
        - better than `name: str = None`
        - gives better autocompletion for your editor (Good tool for developers)


Note: Python requires you to put required parameters in front of optional parameters
- Remedy: Put *
    - Similar to kwargs, allows the function to accept unlimited positional arguments, then treat the rest as positional arguments

Example:

```py
def get_item(*, name: name: Optional[str] = None, test: int):
```

Next: How to combine query parameters AND path parameters!

```py
@app.get("/get-by-name/{item_id}")
def get_item(
    *,
    item_id: int, # not necessary,
    name: Annotated[str, Query(title="Name", description="Name of item.")],
    # name: Optional[str] = None,
    test: int # not necessary
):
    for item_id in inventory:
        if inventory[item_id]["name"] == name:
            return inventory[item_id]
    return {"Data": "Not found"}

```

Test this out quickly: http://127.0.0.1:8000/get-by-name/1?name=Milk&test=2


Why you may want to combine path parameters AND query parameters in a real life scenario:
- You may want to narrow down the results of the GET request (using path parameters only)
    - Example: GET request to the /cars endpoint, ?color=blue to get only blue cars

- Best practice for RESTful API design:
    - path params: identify a specific resource/resource
    - query parameters: sort/filter those resources furthermore

## Request Body + POST Method

POST Method: Add data to the database

Request body: 
- When you add info to a database, you won't send it as query/path parameters
    - You will send a bunch in a request body
- Example: Endpoint that accepts new items
    - Input: BaseModel (from pydantic)
        - Request body
            - This is added to the database

```py
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float
    brand: Optional[str] = None

# Take this Request Body, add it to the inventory
@app.post("/create-item/{item_id}")
def create_item(item_id: int, item: Item):
    if item_id in inventory:
        return {"Error": "Item ID already exists."}
    
    #inventory[item_id] = {"name": item.name, "price": item.price, "brand": item.brand} (old way)
    inventory[item_id] = item
    return inventory[item_id]
```

What is going on here:
- Import dependencies:
    - BaseModel: A base class for creating Pydantic models
        - Pydantic models are simply classes which inherit from BaseModel and define fields as annotated attributes

- Define BaseModel of `Item`
    - Attributes:
        - name
        - price
        - brand (optional)

- Create endpoint: .post("/create-item/{item_id}")
    - POST Method means we are sending a request body
    - We need item_id for saving to a key in the database

- Function definition
    - Input: BaseModel of `Item`
        - When you have this, the FastAPI knows there will be a "request body"
            - No need for path OR query parameters
            - The request body is required for this endpoint/function to work
    
    - Path parameter: {item_id}
        - This is so that we know where to save this `Item` into the database/inventory
        - Make sure to match the path parameter with an input parameter for the Python function below the path/endpoint definition
            - This is required

Try this out!
- Save work
- Head to http://127.0.0.1:8000/docs
- Try it out
    - Enter item_id of 2
    - "name": "Eggs"
    - "price": 4.99
    - "brand": None (remove it, it is optional)

- Check that your response body matches what you just entered in
- Try get_item/2
    - http://127.0.0.1:8000/get-item/2
    - In docs -> Try it out -> 2 -> Execute
        - You should see the same as above

Note: We are only saving these items in memory (not persistent), so everytime you refresh (save your .py file), you will lose your work.


## PUT Method

PUT Method: Update data in the database

```py
class UpdateItem(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    brand: Optional[str] = None

@app.put("/update-item/{item_id}")
def update_item(item_id: int, item: UpdateItem):
    if item_id not in inventory:
        return {"Error": "Item ID does not exist."}

    hashmap_item_data = item.model_dump(exclude_defaults=True)
    inventory[item_id].__dict__.update(hashmap_item_data)
    return inventory[item_id]
```

What is going on here:
- Create endpoint: .put("/update-item/{item_id}")
    - PUT Method means we are sending a request body
    - We need item_id for updating a key in the database

- Function definition
    - Input: BaseModel of `Item`
        - When you have this, the FastAPI knows there will be a "request body"
            - No need for path OR query parameters
            - The request body is required for this endpoint/function to work

    - Path parameter: {item_id}
        - This is so that we know which `Item` to update into the database/inventory
        - Make sure to match the path parameter with an input parameter for the Python function below the path/endpoint definition
            - This is required

    - Updating the existing item in the database: .update(item)
        - item.model_dump(): Turns the item into a Python dictionary
            - Updates only the values you provide
                - In this example, you must pass name/price
                    - Remedy: A new class named `UpdateItem`
                        - This class will make everything optional
            - exclude_defauls=True: makes it so that optional values that end up being None do NOT update the database

        - inventory[item_id].__dict__.update(hashmap_item_data):
            - inventory[item_id]: the BaseModel Item class object
            - .__dict__: allows you to access the values of the class as a dictionary
                - usually it prints as a string type
                    - I believe you have to access each values 1 by 1 with .key syntax
                - this was a struggle before I knew this syntax, as you cannot use brackets
                    - ie. inventory[item_id][key]
            - .update(hashmap_item_data): allows you to update the dict with a new dict of values
                - this is where we take the request body and apply the new values

Testing this out:
- Add an item: http://127.0.0.1:8000/docs -> /create-item -> Try it out
    - item_id = 1
    - name: Milk
    - price: 2.49
    - brand: Kemps
    - Execute!

- Get the item: 
    - http://127.0.0.1:8000/get-item/1
    - http://127.0.0.1:8000/get-by-name/1?name=Milk&test=999

- Update the item: http://127.0.0.1:8000/docs -> /update-item -> Try it out
    - item_id = 1
    - name: Milk (or delete this line of code to see how it handles None values)
    - price: 22.49
    - brand: Designer Brand
    - Execute!

- Get the item: 
    - http://127.0.0.1:8000/get-item/1
    - http://127.0.0.1:8000/get-by-name/1?name=Milk&test=999

Notes:
- When sending JSON, if you have the extra comma at the end of your last row, it will give the following error: "Expecting property name enclosed in double quotes"
- When sending a request body, if you use "null" as a value, with my current code logic, it will turn into None and not make a change to the database.

## DELETE Method

```py
@app.delete("/delete-item")
def delete_item(item_id: int = Query(..., description="The ID of the item we are going to delete.", ge=0)):
    if item_id not in inventory:
        return {"Error": "ID does not exist."}
        
    del inventory[item_id]
    return {"Success": f"Item {item_id} deleted!"}
```

What is going on here:
- Create endpoint: .delete("/delete-item")
    - DELETE Method means we are sending a request body
    - We need item_id for deleting a key in the database

- Function definition
    - item_id
        - Query parameter: I am not certain why we use this but will carry on...
            - Description: Adds text to the docs
            - ge: item_id must be >= 0


Testing this out:
- Add an item: http://127.0.0.1:8000/docs -> /create-item -> Try it out

- Get the item: http://127.0.0.1:8000/get-item/1

- Delete an item:
    - http://127.0.0.1:8000/docs -> /delete-item -> Try it out
        - Works!
    - http://127.0.0.1:8000/delete-item?item_id=1
        - Error: {"detail":"Method Not Allowed"} ...
            - You certainly can’t create a link that uses anything other than GET

- Get the item: http://127.0.0.1:8000/get-item/1
    - Should return nothing...


## Status Codes and Error Responses

```py
from fastapi import FastAPI, Path, Query, HTTPException, status

... raise HTTPException(status_code=404, detail="Item ID does not exist.")
... raise HTTPException(status_code=404, detail="Item name does not exist.")
... raise HTTPException(status_code=400, detail="Item ID already exists.")
... raise HTTPException(status_code=404, detail="Item ID does not exist.")
... raise HTTPException(status_code=404, detail="Item ID does not exist.")

... raise HTTPException(status_code=HTTP.)

```

Import dependencies:
- HTTPException: Allows you to raise 
    - FastAPI backend is waiting for an exception to be raised
        - Once it is, it returns the equivalent HTTP response
- status: 
    - I won't use it, but you can use stuff like `status_code=status.HTTP_404_NOT_FOUND`

- Status code:
    - 400: Bad request
    - 404: Not Found

---

### References

1. [Flask vs. FASTAPI](https://www.reddit.com/r/flask/comments/13pyxie/flask_vs_fastapi/)
2. [FastAPI - Path Parameters and Numeric Validations](https://fastapi.tiangolo.com/tutorial/path-params-numeric-validations/)
3. [typing — Support for type hints](https://docs.python.org/3/library/typing.html)
4. [When do I use path params vs. query params in a RESTful API?](https://stackoverflow.com/questions/30967822/when-do-i-use-path-params-vs-query-params-in-a-restful-api)
5. [Pydantic - BaseModel](https://docs.pydantic.dev/latest/api/base_model/)
6. [Iterate over object attributes in python](https://stackoverflow.com/questions/11637293/iterate-over-object-attributes-in-python)
7. [How to update pydantic model from dictionary?](https://stackoverflow.com/questions/73421846/how-to-update-pydantic-model-from-dictionary)
8. [How to specify DELETE method in a link or form?](https://stackoverflow.com/questions/6926512/how-to-specify-delete-method-in-a-link-or-form)