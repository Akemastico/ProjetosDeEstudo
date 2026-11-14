from decimal import MAX_EMAX

from django.db import models
from devs.models import Developer

class Categories(models.Model):
    name = models.CharField(max_length=50, unique=True)

class Tasks(models.Model):
    title = models.CharField(max_length=100)
    developer = models.ForeignKey(Developer,on_delete=models.CASCADE,related_name="tasks")
    description = models.CharField(max_length=500)
    categories = models.ManyToManyField(Categories,related_name="categories")    
    
