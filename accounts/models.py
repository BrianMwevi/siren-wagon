from sirenapp.models import CustomerAccount, Package
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save


# Create your models here.
class User(AbstractUser):
    email = models.EmailField(max_length=255, unique=True)
    phone = models.CharField(max_length=200, unique=True)
    account = models.ForeignKey(
        CustomerAccount, blank=True, related_name='account', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.username.title()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phone']


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
        return self.user.username


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


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        account = CustomerAccount.objects.get(account_holder=instance)
        profile = PatientProfile.objects.create(user=instance, account=account)
