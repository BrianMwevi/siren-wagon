from sirenapp.models import CustomerAccount, Package
from django.contrib.auth.models import AbstractUser
from django.db import models
<<<<<<< HEAD
from django.contrib.auth.models import AbstractUser,BaseUserManager
from rest_framework.authtoken.models import Token
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
=======


>>>>>>> f221cdb1a78fe7fa33aa953c9eadf9fea5d4f8e8
# Create your models here.
class User(AbstractUser):
    first_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    username = models.CharField(
        max_length=200, blank=True, null=True, unique=True)
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=200, blank=True, null=True)
    password = models.CharField(max_length=255)

    account = models.ForeignKey(
        CustomerAccount, blank=True, related_name='account', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.username


<<<<<<< HEAD
    
    

    
=======
USERNAME_FIELD = 'email'
REQUIRED_FIELDS = ['username']
>>>>>>> f221cdb1a78fe7fa33aa953c9eadf9fea5d4f8e8


class PatientProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="patient")
    picture = models.ImageField(blank=True, null=True)
    emergency_contact = models.ManyToManyField(
        'EmergencyContact', related_name='emergency_contact')
    package = models.ForeignKey(
        Package, related_name='patient_packages', on_delete=models.CASCADE)
    medical_conditions = models.CharField(
        max_length=200, blank=True, null=True)

    def __str__(self):
        return self.user.username


class EmergencyContact(models.Model):
    first_name = models.CharField(max_length=55)
    last_name = models.CharField(max_length=55)
    email = models.EmailField(max_length=255)
    phone1 = models.CharField(max_length=255)
    phone2 = models.CharField(max_length=255, blank=True, null=True)
    phone3 = models.CharField(max_length=255, blank=True, null=True)
    relationship = models.CharField(max_length=55)

    def __str__(self):
        return f"{self.first_name} {self.last_name}: {self.relationship}"
