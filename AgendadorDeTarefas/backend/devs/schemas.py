from ninja import Schema
from pydantic import EmailStr


class RespOut(Schema):
    name: str
    email: EmailStr
    
    
class DevIn(Schema):
    name:str
    email:EmailStr
    password: str
    
class DevTaskOut(Schema):
    title:str
    description:str | None
    
    