from django.db import models
from core.settings import AUTH_USER_MODEL
from django.utils import timezone


class Account(models.Model):
    account_holder = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.CASCADE)
    account_number = models.PositiveBigIntegerField(
        unique=True, blank=True, null=True)
    balance = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.account_number


class Sender(models.Model):
    sender = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.CASCADE)
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE)
    account_number = models.PositiveBigIntegerField(
        unique=True, blank=True, null=True)

    def __str__(self):
        return self.sender.username


class Reciever(models.Model):
    reciever = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.CASCADE)
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE)
    account_number = models.PositiveBigIntegerField(
        unique=True, blank=True, null=True)

    def __str__(self):
        return self.reciever.username


class Transaction(models.Model):
    sender = models.ForeignKey(
        Sender, on_delete=models.CASCADE)
    reciever = models.ForeignKey(
        Reciever, on_delete=models.CASCADE)
    account_number = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=0)
    trans_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.trans_date


class Profile(models.Model):
    picture = models.ImageField(blank=True, null=True)
    username = models.CharField(max_length=200, blank=True, null=True)
    emergency_contact = models.CharField(max_length=200, blank=True, null=True)
    package = models.ForeignKey('Package', on_delete=models.CASCADE)
    medical_conditions = models.CharField(
        max_length=200, blank=True, null=True)
    account_number = models.ForeignKey('Account', on_delete=models.CASCADE)
    trip = models.ForeignKey('Trip', on_delete=models.CASCADE)
    availability = models.BooleanField('available', default=False)
    plate_number = models.CharField(max_length=200, blank=True, null=True)
    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.username


class Package(models.Model):
    CHOICES = [
        ('regular', 'regular'),
        ('premium', 'premium'),
    ]
    package_choice = models.CharField(
        max_length=200, choices=CHOICES, default="regular")
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.package_choice


class Trip(models.Model):
    trip_date = models.DateTimeField(default=timezone.now)
    driver = models.ForeignKey(
        AUTH_USER_MODEL, related_name='driver', on_delete=models.CASCADE)
    fee = models.ForeignKey(
        'Transaction', related_name='trip_fee', on_delete=models.CASCADE)
    pickup = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)

    def __str__(self):
        return self.trip_date
