from datetime import datetime
from pydantic import BaseModel


class Farmer(BaseModel):
    firstname: str
    lastname: str
    farmname: str
    address: str
    email: str

    class Config:
        orm_mode = True
