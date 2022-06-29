from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):

    first_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    username = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=200, blank=True, null=True)
    service_provider = models.BooleanField('Is_lender', default=False)
    client = models.BooleanField('Is_applicant', default=False)

    def __str__(self):
        return self.username


# user.name
