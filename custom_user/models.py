from django.db import models
from django.contrib.auth.models import AbstractUser
from custom_user.utils import CustomUserManager


class User(AbstractUser):
    email = models.EmailField(unique=True) 
    first_name = models.CharField(max_length=50)   
    last_name = models.CharField(max_length=50) 
    date_joined = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    username = None
    
    REQUIRED_FIELDS= ["first_name", "last_name"]
    USERNAME_FIELD = "email"

    objects = CustomUserManager()



    