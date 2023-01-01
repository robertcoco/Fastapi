#pythonthings
from typing import Optional
from enum import Enum
from datetime import date

#pydantic
from pydantic import BaseModel, Field, EmailStr, PastDate

#Fastapi
from fastapi import FastAPI, status
from fastapi import Body, Query, Path, Form, Header, Cookie

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
    
class PersonBase(BaseModel):
    first_name: str = Field(
        ...,
        title = "First name ",
        description = "First name of the person",
        min_length = 1,
        max_length = 50
        )

    last_name: str =  Field(
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

    born_date: PastDate = Field(default = None)

    email: EmailStr = Field(default = None)

class PersonOut(PersonBase):
    pass

class Person(PersonBase):
    
    class Config:
        schema_extra = {
            "example": {
                "first_name": "Roberto Angel",
                "last_name": "Abad De Los Santos",
                "age": 19,
                "hair_color": "black",
                "is_married": False,
                "password": "yoyinaguahace",
                "email": "perdonholaperdon123@gmail.com",
                "account_money": 4556.5767,
                "born_date":  date(2003, 8, 18)
            }
        }
    password: str = Field(..., min_length = 8)

class LoggingOut(BaseModel):
    username: str = Field(
        ..., 
        max_length = 20,
        example = "angelo495"
        )
    message: str = Field(default = "Logged susccesfully")

app = FastAPI()

@app.get(
    path = "/",
    status_code = status.HTTP_200_OK 
    )
def home():
     return {"Hello": "World"}


# Request and Response body
@app.post(
    path = "/person/new",
    response_model = PersonOut,
    status_code = status.HTTP_201_CREATED
    )
def create_person(person: Person = Body(...)):
    return person

#Validaciones: query parameters
@app.get(
    path = "/person/detail",
    status_code = status.HTTP_200_OK
    )
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
@app.get(
    path = "/person/datail/{person_id}",
    status_code = status.HTTP_200_OK
    )
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
@app.put(
    path = "/person/{person_id}",
    status_code = status.HTTP_200_OK
    )
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


# Form logging
@app.post(
    path = "/login",
    # response model to ignore some information we dont want to send to the client
    response_model = LoggingOut,
    status_code = status.HTTP_200_OK
    )
def Login(
    username: str = Form(...),
    password: str = Form(...)
):
    return LoggingOut(username = username)

# Cookies and headers parameters

@app.post(
    path = "/contact",
    status_code = status.HTTP_200_OK,
)
def contact(
    first_name: str = Form(
        ...,
        example = "Roberto Angel",
        min_length = 1,
        max_length = 50 
        ),
    last_name: str = Form(
        ...,
        max_length= 50,
        min_length = 1,
        example = "Abad De Los Santos"
        ),
    user_agent: Optional[str] = Header(default = None),
    ads: Optional[str] = Cookie(default = None),
    Email: EmailStr = Form(
        ...,
        example = "perdonholaperdon123@gmail.com"
        )
):
    return user_agent