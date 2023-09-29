from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
from vendor.hubspot.client import APIClient as HubspotAPIClient
import re
from django.core.exceptions import ValidationError

# Create your models here.
class CustomUser(AbstractUser):
    username= models.CharField(max_length=200 , null=True ,blank=True)
    email = models.EmailField(unique=True)
    forget_password_token= models.CharField(max_length=255,  null=True , blank=True)
    profile_img = models.ImageField(upload_to="profile_imgs", null=True , blank=True)
    phone_number = models.CharField(
        verbose_name='Phone Number',
        help_text='Enter your phone number in international format (e.g., +1234567890).',
        null=True,
        blank=True,
    )

    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS=[]
    objects = CustomUserManager()
    # helllo 

    def __str__(self):
        return self.email
    
    def validate_phone_number(self):
        phone_number_pattern = r'^\+\d{10,15}$'  
        if not re.match(phone_number_pattern, str(self.phone_number)):
            print('Invalid phone number format. Please use international format, e.g., +1234567890')
            raise ValidationError('Invalid phone number format. Please use international format, e.g., +1234567890.')
            
    def clean(self):
        super().clean()
        self.validate_phone_number()
    
    @property
    def user_email(self):
        return self.email   
    
    def send_to_hubspot(self):
        api = HubspotAPIClient()
        api.create_or_update_contact({
            "email": self.email,
            
        })


    
