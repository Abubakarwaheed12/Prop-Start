from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager


# Create your models here.
class CustomUser(AbstractUser):
    username= None
    email = models.EmailField(unique=True)
    forget_password_token= models.CharField(max_length=255, default="")
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS=[]
    objects = CustomUserManager()
    # helllo 

    def __str__(self):
        return self.email
    



    
