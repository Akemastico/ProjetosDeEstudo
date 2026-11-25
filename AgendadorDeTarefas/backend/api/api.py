from ninja_extra import NinjaExtraAPI
from tasks.views import TaskController
from ninja_jwt.controller import NinjaJWTDefaultController
from devs.views import DevController, Developer


app = NinjaExtraAPI()
app.register_controllers(TaskController,NinjaJWTDefaultController,DevController)

@app.get("")
def home(request):
    return {"status" : "ok"}




