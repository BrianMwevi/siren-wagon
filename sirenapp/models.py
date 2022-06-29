from datetime import date
from time import time
from django.db import models
from pytz import timezone
from accounts.models import User
from django.utils import timezone

class Account(models.Model):
    account_holder = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_account')
    account_number = models.PositiveBigIntegerField( unique=True,blank=True, null=True)
    balance = models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.account_number

    
class Transaction(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sender')
    reciever = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reciever')
    account_number = models.ForeignKey('Account', on_delete=models.CASCADE, related_name='sender')
    amount = models.PositiveIntegerField(default=0)
    trans_date=models.DateTimeField(default=timezone.now())
    
    def __str__(self):
        return self.trans_date
 

class Profile(models.Model):
    picture = models.ImageField(blank=True,null=True)
    username = models.CharField(max_length=200, blank=True, null=True)
    emergency_contact= models.CharField(max_length=200, blank=True, null=True)
    package= models.ForeignKey('Package', on_delete=models.CASCADE, related_name='user_package')
    medical_conditions= models.CharField( max_length=200, blank=True, null=True)
    account_number =models.ForeignKey('Account', on_delete=models.CASCADE, related_name='user_account')
    trip =models.ForeignKey('Trip', on_delete=models.CASCADE,related_name='user_trips')
    availability=models.BooleanField
    user=models.OneToOneField('User', related_name='profile',on_delete=models.CASCADE)

    def __str__(self):
        return self.username


class Package(models.Model):
    CHOICES=[
       ( 'regular','regular'),
       ('premium','premium'),
    ]
    package_choice=models.CharField(choices=CHOICES,default="regular")
    user = models.ForeignKey('User', related_name='user_package',on_delete=models.CASCADE)


    def __str__(self):
        return self.package_choice


class Trip(models.Model):
    trip_date=models.DateTimeField(default=timezone.now())
    driver = models.ForeignKey('User', related_name='profile',on_delete=models.CASCADE)
    fee= models.ForeignKey('Transaction', related_name='trip_fee',on_delete=models.CASCADE)
    

    def __str__(self):
        return self.trip_date

