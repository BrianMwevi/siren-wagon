from sirenapp.models import Ambulance, CustomerAccount, Package
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(max_length=255, unique=True)
    phone = models.CharField(max_length=200, unique=True)

    account = models.ForeignKey(
        CustomerAccount, blank=True, related_name='account', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.username.title()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phone']


class DriverProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="driver_profile")
    id_number = models.PositiveIntegerField(unique=True)
    driving_license = models.CharField(max_length=55, unique=True)
    picture = models.ImageField(
        upload_to='images/', default="images/avatar_wqbvxp.svg")
    ambulance = models.ForeignKey(
        Ambulance, related_name='driver_ambulance', on_delete=models.CASCADE, null=True, blank=True)
    updated_date = models.DateTimeField(auto_now=True)
    availability = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"Driver: {self.user.username.title()}"


class DoctorProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="doctor_profile")
    id_number = models.PositiveIntegerField(unique=True)
    picture = models.ImageField(
        upload_to='images/', default="images/avatar_wqbvxp.svg")
    ambulance = models.ForeignKey(
        Ambulance, related_name='doctor_ambulance', on_delete=models.CASCADE, null=True, blank=True)
    availability = models.BooleanField(default=False)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"Doctor: {self.user.username.title()}"


class PatientProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="patient")
    id_number = models.PositiveIntegerField(null=True, blank=True)
    picture = models.ImageField(
        upload_to='images/', default="images/avatar_wqbvxp.svg")
    emergency_contacts = models.ManyToManyField(
        'EmergencyContact', related_name='emergency_contact', blank=True)
    package = models.ForeignKey(
        Package, related_name='patient_packages', on_delete=models.CASCADE, null=True, blank=True)
    medical_conditions = models.CharField(
        max_length=200, blank=True, null=True)
    account = models.ForeignKey(
        CustomerAccount, blank=True, related_name='patient_account', null=True, on_delete=models.CASCADE)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Patient: {self.user.username.title()}"


class EmergencyContact(models.Model):
    patient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="patient_emergency", null=True, blank=True)
    first_name = models.CharField(max_length=55)
    last_name = models.CharField(max_length=55)
    email = models.EmailField(max_length=255, null=True, blank=True)
    id_number = models.PositiveIntegerField()
    phone1 = models.CharField(max_length=255)
    phone2 = models.CharField(max_length=255, blank=True, null=True)
    phone3 = models.CharField(max_length=255, blank=True, null=True)
    relationship = models.CharField(max_length=55)

    def __str__(self):

        return f"{self.first_name} {self.last_name}: {self.relationship}"
