#pythonthings
from typing import Optional
from enum import Enum

#pydantic
from pydantic import BaseModel, Field, EmailStr, PastDate

#Fastapi
from fastapi import FastAPI
from fastapi import Body, Query, Path

class HairColor(Enum):
    white = "white"
    brown = "brown"
    black = "black"
    blonde = "blonde"
    red = "red"

class Location(BaseModel):
    city: str = Field(
        ...,
        title = "City ",
        description = "City of the person",
        min_length = 1,
        max_length = 60,
        example = "San Cristóbal"
    )
    state: str = Field(
        ...,
        title = "State",
        description = "state of the person",
        min_length = 1,
        max_length = 60,
        example = "San Cristóbal"
        )
    country: str = Field(
        ...,
        title = "Country",
         example = "R.D"
        )
    


class Person(BaseModel):
    first_name: str = Field(
        ...,
        title = "First name ",
        description = "First name of the person",
        min_length = 1,
        max_length = 50
        )

    second_name: str =  Field(
        ...,
        title = "First name ",
        description = "First name of the person",
        min_length = 1,
        max_length = 50
        )

    age: int = Field(
        ...,
        ge = 0,
        lt = 120
        )

    account_money: Optional[float] = Field(defalut = None)

    hair_color: Optional[HairColor] = Field(default = None)

    is_married: Optional[bool] = Field(default = None)

    born_date: PastDate

    email: EmailStr 

    class Config:
        schema_extra = {
            "example": {
                "first_name": "Roberto Angel",
                "last_name": "Abad De Los Santos",
                "age": 19,
                "hair_color": "black",
                "is_married": False
            }
        }

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
        description= "This is the person name. The number of characters must be between 1 and 50",
         example = "Angel"
        ),
    age: int = Query(
        ...,
        title = "Person age",
        description = "This is the person age. It's required",
         example = 12
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
        description = "This is the identifier of the person. These parameter must be greater than 0",
        example = 12
        )
):
    return{person_id: "It is person"}

#validaciones: resquest body
@app.put("/person/{person_id}")
def update_person(
    person_id: int = Path(
        ...,
        title = "Person id",
        description = "This is person id. It's required",
        example = 38
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