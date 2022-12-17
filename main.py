#pythonthings
from typing import Optional

#pydantic
from pydantic import BaseModel

#Fastapi
from fastapi import FastAPI, Body, Query


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
@app.get("person/detali")
def show_person(
    name: Optional[str] = Query(None, min_length=1, max_length=50),
    age: str = Query(...)
):
    return{name: age}



