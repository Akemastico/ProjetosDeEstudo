from django.http import HttpResponse
from ninja.errors import HttpError
from ninja_extra import api_controller, ControllerBase, route
from tasks.models import Tasks
from .models import Developer
from .schemas import DevIn
from ninja_jwt.authentication import JWTAuth


@api_controller("/devs")
class DevController(ControllerBase):

    @route.get("/list")
    def listDevs(self):
        users = Developer.objects.order_by("-id")[:10]
        return [{"name": dev.username, "email": dev.email} for dev in users]

    @route.post("/create")
    def createDev(self, payload: DevIn):
        if Developer.objects.filter(email=payload.email).exists():
            raise HttpError(409, "Email already registered")
        Developer.objects.create_user(
            username=payload.name,
            email=payload.email,
            password=payload.password,
        )
        return HttpResponse("usuario criado com sucesso", status=201)

    @route.get("/dev/me", auth=JWTAuth())
    def get_user_tasks(self):
        developer = Developer.objects.get(
            username=self.context.request.user
        )
        data = Tasks.objects.filter(devname=developer).order_by("-id")
        return [{"title": i.title, "description": i.description} for i in data]
