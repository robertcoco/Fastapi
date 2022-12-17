#pythonthings
from typing import Optional

#pydantic
from pydantic import BaseModel

#Fastapi
from fastapi import FastAPI
from fastapi import Body, Query, Path

class Location(BaseModel):
    city: str
    state: str
    country: str

class Person(BaseModel):
    first_name: str
    second_name: str
    age: int
    hair_color: Optional[str] = None
    is_married: Optional[bool] = None

app = FastAPI()

@app.get("/")
def home():
     return {"Hello": "World"}


# Request and Response body
@app.post("/person/new")
def create_person(person: Person = Body(...)):
    return person

#Validaciones: query parameters
@app.get("/person/detail")
def show_person(
    name: Optional[str] = Query(
        None,
        min_length=1,
        max_length=50,
        title = "Person name",
        description= "This is the person name. The number of characters must be between 1 and 50"
        ),
    age: str = Query(
        ...,
        title = "Person age",
        description = "This is the person age. It's required"
        )
):
    return{name: age}

#Validaciones: path parameters
@app.get("/person/datail/{person_id}")
def show_person_id(
    person_id: int = Path(
        ..., 
        ge=1,
        title = "Person id",
        description = "This is the identifier of the person. These parameter must be greater than 0"
        )
):
    return{person_id: "It is person"}

#validaciones: resquest body
@app.put("/person/{person_id}")
def update_person(
    person_id: int = Path(
        ...,
        title = "Person id",
        description = "This is person id. It's required"
        ),
    person: Person = Body(
        ...,
        title = "Person information",
        description = "person personal information"
        ),
    location: Location = Body(
        ...,
        title = "Location information",
        description = "Person location"
        )
):
    results = person.dict()
    results.update(location.dict())
    return results