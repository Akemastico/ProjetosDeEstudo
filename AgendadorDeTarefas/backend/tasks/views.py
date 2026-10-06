from ninja_extra import api_controller,ControllerBase,route
from typing import List
from .schemas import TaskIn
from django.shortcuts import get_list_or_404
from .models import Tasks



@api_controller("/tasks")
class TaskController(ControllerBase):
    
    @route.get("/health")
    def healthCheck(self):
        return {"status": "ok"}
    
    @route.get("/list")
    def listTasks(self) -> List[TaskIn]:
        tasks = get_list_or_404(Tasks)
        return tasks
    
    @route.post("/create")
    def createTask():
        ...



