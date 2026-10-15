
from django.contrib.auth.models import AbstractUser

class UsersModel(AbstractUser):
    def __str__(self):
        return f'User : {self.username}'


    
    
