from ninja_extra import NinjaExtraAPI
from tasks.views import TaskController

app = NinjaExtraAPI()
app.register_controllers(TaskController)


