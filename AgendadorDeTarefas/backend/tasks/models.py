from django.db import models
from django.conf import settings

class Tasks(models.Model):
    class Categories(models.IntegerChoices):
        ESPORTE = 1,"esporte"
        ESTUDO = 2,"estudo"
        LUTA = 3,"luta"
        RELACIONAMENTO = 4,"relacionamento"
        
    title = models.CharField(max_length=100)
    devname = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="tasks")
    description = models.CharField(max_length=500)
    categories = models.IntegerField(choices=Categories.choices)   
    
