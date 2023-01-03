#PythonThings
from typing import Optional
from enum import Enum
from datetime import date

#Pydantic
from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr, PastDate

#Fastapi
from fastapi import FastAPI, status
from fastapi import Body, Query, Path, Form, Header, Cookie, UploadFile, File
from fastapi import HTTPException


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
    path = "/home",
    status_code = status.HTTP_200_OK,
    tags = ["Home"],
    summary = "Returns a json file hello world"
    )
def home():
    """
    Say hello world 

    Say hello world to the user 

    Parameters:

        - No parameters
    
    Returns a json file with a key hello and value world
    """
    return {"Hello": "World"}


# Request and Response body
@app.post(
    path = "/person/new",
    response_model = PersonOut,
    status_code = status.HTTP_201_CREATED,
    tags = ["Persons"],
    summary = "Create a person in the app"
    )
def create_person(person: Person = Body(...)):
    """
    Create a person

    This path operation creates a person in the app and save it the database

    Parameters:

        - Request body parameters:

            - **person: Person -> a person model with first name, last name, age, hair color, marital status and password**
    
    Returns a person model with first name, last name, age, hair color, marital status
    """
    return person

#Validaciones: query parameters
@app.get(
    path = "/person/detail",
    status_code = status.HTTP_200_OK,
    tags = ["Persons"],
    summary = "this gets the name and the age of the person from query parameter and then show it",
    depracated = True
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
    """
    Get person basic information

    This gets the name and the age of the person 

    Parameters:

        - Query parameters:

            - **name: name the of the person**
            - **age : age of the person**
    
    Returns the name and the age of the person
    """
    return{name: age}

#Validaciones: path parameters

persons = [1, 2, 3, 4, 6]

@app.get(
    path = "/person/datail/{person_id}",
    status_code = status.HTTP_200_OK,
    tags = ["Persons"],
    summary= "Gets and return the person id "
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
    if person_id not in persons:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "The person doesn't exist"
        )
    return{person_id: "It is person"}

#validaciones: resquest body
@app.put(
    path = "/person/{person_id}",
    status_code = status.HTTP_200_OK,
    tags = ["Persons"],
    summary = "Gets the person information"
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
    """
    Update the person information

    Update the person information that includes the first name, last name, age, hair color, marital status, location 

    Parameters:

        - Path parameters:

            - **Person id: the identifier of the person**
            
        - Request body parameters:
        
            - **person: person information read above**

    Returns the person information
    """
    results = person.dict()
    results.update(location.dict())
    return results


# Form logging
@app.post(
    path = "/login",
    # response model to ignore some information we dont want to send to the client
    response_model = LoggingOut,
    status_code = status.HTTP_200_OK,
    tags = ["Login"],
    summary = "Log a person in the application"
    )
def Login(
    username: str = Form(...),
    password: str = Form(...)
):
    """
    User Logging

    Get the user's username and the user's password

    Parameters:

        - Form parameters: 

            - **username**
            - **password**
    
    Returns the username
    """
    return LoggingOut(username = username)

# Cookies and headers parameters

@app.post(
    path = "/contact",
    status_code = status.HTTP_200_OK,
    tags = ["Contact"],
    summary = "Get the contact information of a persone"
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
    """
    Person contact inforamtion

    Get the contact inforamtion of a particular person

    Parameters:

        - Form parameters:

            - ** first name **
            - ** last name **
        
        - Cookie:

            - ** ads: informacion para anuncios **
        
        - Header: 

            - ** user agent: user pc's information
    
    Returns the user agent information
    """
    return user_agent

@app.post(
    path = "/postimage",
    status_code = status.HTTP_200_OK,
    tags = ["PostImage"],
    summary = "Get the inforamtion of a uploaded file"
)
def post_image(
    image: UploadFile = File(...)
):
    """
    File information

    Get the inforamation of a file

    Parameters: 

        - File parameter:

            - ** image **
    """
    return {
        "Filename": image.filename,
        "Format": image.content_type,
        "Size(kb)": round(len(image.file.read())/1024, ndigits = 2)
    }