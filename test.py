from typing import Set, Union, List
from enum import Enum
from fastapi import FastAPI, Body, status, HTTPException
from pydantic import BaseModel, EmailStr

app = FastAPI()


class Image(BaseModel):
    name: str
    url: str


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None
    tags: List[str] = []
    # Unique list
    image: Union[Image, None] = None
    utags: Set[str] = set()

    class Config:
        schema_extra = {
            "example": {
                "name": "Iphone",
                "description": "A very nice Item",
                "price": 35.4,
                "image": "image url",
            }
        }


class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Union[str, None] = None


class UserIn(UserBase):
    password: str


class UserOut(UserBase):
    pass


class UserInDB(UserBase):
    hashed_password: str


def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password


def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_dict = user_in.dict()
    user_in_db = UserInDB(
        username=user_dict["username"],
        hashed_password=hashed_password,
        email=user_dict["email"],
        full_name=user_dict["full_name"],
    )
    print("User saved! ..not really")
    return user_in_db


@app.post("/user/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user_data(user_in: UserIn):
    user_saved = fake_save_user(user_in)
    return user_saved


@app.post("/user/", response_model=UserOut)
async def create_user(user: UserIn):
    return user


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


fake_items_db = [{"item_name": "Foo"}, {
    "item_name": "Bar"}, {"item_name": "Baz"}, {"item_name": "Phone"}, {"item_name": "Tablete"}]


@app.get("/items/{skip}/{limit}")
async def read_item(skip: int, limit: int):
    if limit - skip > 10:
        return {"error": "you're allowed to see only 10 items"}
    return fake_items_db[skip: skip + limit]


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item = Body(embed=True)):
    results = {"item_id": item_id, "item": item}
    return results

# ### Get Something Base on Enums
# @app.get("/models/{model_name}")
# async def get_model(model_name: ModelName):
#     if model_name.value == "alexnet":
#         return {"model_name": model_name, "message": "Deep Learning FTW!"}

#     if model_name.value == "lenet":
#         return {"model_name": model_name, "message": "LeCNN all the images"}

#     return {"model_name": model_name, "message": "Have some residuals"}


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}


items = {"id": 5, "foo": "The Foo Wrestlers"}


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id != items["id"]:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item": items["id"]}
