from django import tasks
from ninja_extra import api_controller,ControllerBase,route
from ninja_jwt.authentication import JWTAuth
from .schemas import TaskIn
from .models import Tasks
from devs.models import Developer
from ninja.errors import HttpError


@api_controller("/tasks")
class TaskController(ControllerBase):
    
    @route.get("/health")
    def healthCheck(self):
        return {"status": "ok"}

    @route.post("/create",auth=JWTAuth())
    def createTask(self,payload:TaskIn):
        developer = self.get_object_or_exception(
            Developer,
            username=self.context.request.user
        )
        if Tasks.objects.filter(title=payload.title, devname=developer).exists():
            raise HttpError(409, "Task name already saved")
            
        task = Tasks.objects.create(title=payload.title, devname=developer,description=payload.description,categories=payload.categories)   
        
        return {"status" : 201, "name" : task.title}
    
    
        
        



