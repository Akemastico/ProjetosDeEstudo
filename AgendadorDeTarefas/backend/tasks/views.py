from ninja_extra import api_controller,ControllerBase,route
from typing import List

from ninja_jwt.authentication import JWTAuth
from .schemas import TaskIn
from django.shortcuts import get_list_or_404
from .models import Tasks
from devs.models import Developer



@api_controller("/tasks")
class TaskController(ControllerBase):
    
    @route.get("/health")
    def healthCheck(self):
        return {"status": "ok"}
    
    @route.get("/list",auth=JWTAuth)
    def listAllTasks(self):
        #data = data dos objetos
        data = Tasks.objects.all()
        return data 
        
    @route.post("/create",auth=JWTAuth)
    def createTask(self,payload:TaskIn):
        developer = self.get_object_or_exception(
            Developer,
            developer=self.context.request.user
        )
        task = Tasks.objects.create(title=payload.title, developer=developer,description=payload.description)
        
        if payload.categories:
            task.categories.set(payload.categories)
        
        return {"status" : 201, "name" : task.title}
    
    
        
        



