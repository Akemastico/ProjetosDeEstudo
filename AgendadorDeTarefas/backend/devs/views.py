from django.http import HttpResponse
from ninja.errors import HttpError
from ninja_extra import api_controller,ControllerBase,route
from tasks.models import Tasks
from django.shortcuts import get_list_or_404
from .models import Developer
from schemas import DevIn
from ninja_jwt.authentication import JWTAuth


@api_controller("/devs")
class DevController(ControllerBase):
    
    @route.get("/list")
    def listDevs(self):
        users = Developer.objects.order_by('-id')[:10]
        objects = get_list_or_404(users)
        return [
            {"name" : dev.name,
             "email": dev.email}
            for dev in objects]
    
    @route.post("/create")
    def createDev(self,payload:DevIn):
        if Developer.objects.filter(email=payload.email).exists():
            raise HttpError(409,"Email already registered")
        dev = Developer.objects.create(*payload)
        return HttpResponse(201, "usuario criado com sucesso")
    
    @route.get("/dev/{dev_id}",auth=JWTAuth)
    def get_user_tasks(self, dev_id:int):
        data = Tasks.objects.filter(developer_id=dev_id)
        return data
            
    