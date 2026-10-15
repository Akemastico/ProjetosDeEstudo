from django.db import models
from users.models import UsersModel
from django.conf import settings

class AnotationModel(models.Model):
    text = models.TextField(max_length=1000)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="anotations")
