from ninja_extra import NinjaExtraAPI
from tasks.views import TaskController
from ninja_jwt.controller import NinjaJWTDefaultController

app = NinjaExtraAPI()
app.register_controllers(TaskController,NinjaJWTDefaultController)

@app.get("")
def home(request):
    return {"status" : "ok"}




