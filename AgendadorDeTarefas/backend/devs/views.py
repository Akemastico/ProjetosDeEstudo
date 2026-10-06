from ninja_extra import api_controller,ControllerBase,route
from tasks.models import Tasks
from .models import Developer
from django.shortcuts import get_list_or_404



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
    def createDev(self)
    