from typing import List
from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
from rest_framework.authtoken.models import Token
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
# Create your models here.

class User(AbstractUser):

    first_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    password=models.CharField(max_length=255)
    phone = models.CharField(max_length=200, blank=True, null=True)
    service_provider = models.BooleanField('service_provider', default=False)
    client = models.BooleanField('client', default=False)
    email = models.CharField(max_length=255, unique=True)
    username = models.CharField(max_length=255,blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


    
    

    


# user.name
