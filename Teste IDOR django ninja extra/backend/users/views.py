from ninja_extra import api_controller,route,ControllerBase
from ninja import Schema
from pydantic import EmailStr
from ninja_jwt.authentication import JWTAuth
from .models import UsersModel
from ninja.errors import HttpError
from anotations.models import AnotationModel

class UserIn(Schema):
    name: str
    password: str
    email: EmailStr
    
@api_controller("/user")
class UserController(ControllerBase):

    @route.post('/register')
    def register(self,payload:UserIn):
        if UsersModel.objects.filter(email=payload.email).exists():
            raise HttpError(409, "email ja cadastrado")
        data = payload.model_dump()
        user = UsersModel.objects.create(**data)
        return f'user {user.username} created'
    
    
    @route.get("/selfan",auth=JWTAuth())
    def listOwnAn(self):
        return list(
            AnotationModel.objects.filter(author=self.context.request.user).values("id","text")
        )
    
    
    
    
    
    
    
                       
    
