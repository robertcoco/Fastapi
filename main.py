#pythonthings
from typing import Optional

#pydantic
from pydantic import BaseModel

#Fastapi
from fastapi import FastAPI
from fastapi import Body, Query, Path


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
def create_perseon(person: Person = Body(...)):
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

