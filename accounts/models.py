from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager

# Create your models here.
class CustomUser(AbstractUser):
    username= models.CharField(max_length=200 , null=True ,blank=True)
    email = models.EmailField(unique=True)
    forget_password_token= models.CharField(max_length=255,  null=True , blank=True)
    profile_img = models.ImageField(upload_to="profile_imgs", null=True , blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS=[]
    objects = CustomUserManager()
    # helllo 

    def __str__(self):
        return self.email
    
    @property
    def user_email(self):
        return self.email   




    
