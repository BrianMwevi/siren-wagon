from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):

    first_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    username = models.CharField(max_length=200, blank=True, null=True,unique=True)
    phone = models.CharField(max_length=200, blank=True, null=True)
    service_provider = models.BooleanField('service_provider', default=False)
    client = models.BooleanField('client', default=False)

    def __str__(self):
        return self.username


# user.name
