from django.db import models
from devs.models import Developer

class Categories(models.Model):
    name = models.CharField(max_length=50, unique=True)

class Tasks(models.Model):
    developer = models.ForeignKey(Developer,on_delete=models.CASCADE,related_name="tasks")
    categories = models.ManyToManyField(Categories,related_name="categories")    
    
