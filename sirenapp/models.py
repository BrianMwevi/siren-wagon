from django.db import models
from core.settings import AUTH_USER_MODEL
from django.dispatch import receiver
from django.db.models.signals import post_save


class Hospital(models.Model):
    owner = models.ForeignKey(
        AUTH_USER_MODEL, related_name='owner', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, unique=True)
    location = models.CharField(max_length=255)
    patients = models.ManyToManyField(
        AUTH_USER_MODEL, related_name='patients', blank=True)
    ambulances = models.ManyToManyField(
        'Ambulance', related_name='ambulances', blank=True)
    established_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    doctors = models.ManyToManyField(
        'Doctor', related_name='doctors', blank=True)
    reviews = models.ManyToManyField(
        'Review', related_name='reviews', blank=True)
    account = models.ForeignKey(
        'CustomerAccount', blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Ambulance(models.Model):
    availability = models.BooleanField('available', default=False)
    number_plate = models.CharField(max_length=200, blank=True, null=True)
    trips = models.ManyToManyField(
        'Trip', blank=True, related_name='trips')


class Doctor(models.Model):
    first_name = models.CharField(max_length=55)
    last_name = models.CharField(max_length=55)
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=255)
    ambulance = models.ForeignKey(
        Ambulance, on_delete=models.CASCADE, related_name="doctor_ambulance")


class Driver(models.Model):
    first_name = models.CharField(max_length=55)
    last_name = models.CharField(max_length=55)
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=255)
    ambulance = models.ForeignKey(
        Ambulance, on_delete=models.CASCADE, related_name="driver_ambulance")


class CustomerAccount(models.Model):
    account_holder = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.CASCADE)
    account_number = models.PositiveBigIntegerField(
        unique=True, blank=True, null=True)
    balance = models.PositiveIntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def generate_account_number():
        import random
        import string
        account_number = "".join(random.choice(string.digits)
                                 for _ in range(0, 12))
        return account_number

    def __str__(self):
        return f"{self.account_holder.username}: {self.account_number}"


class Transaction(models.Model):
    sender = models.ForeignKey(
        AUTH_USER_MODEL, related_name='sender', on_delete=models.CASCADE)
    receiver = models.ForeignKey(
        AUTH_USER_MODEL, related_name='receiver', on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=0)
    trans_date = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender.username} TO {self.receiver.username}"


class Package(models.Model):
    CHOICES = [
        ('1', 'regular'),
        ('2', 'premium'),
    ]
    package_choice = models.CharField(
        max_length=200, choices=CHOICES, default="regular")
    amount = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.package_choice


class Trip(models.Model):
    pickup = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    persons = models.PositiveIntegerField(default=3)
    fee = models.ForeignKey(
        'Transaction', related_name='trip_fee', on_delete=models.CASCADE)
    trip_date = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.pickup} TO {self.destination}"


class Review(models.Model):
    user = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews")
    hospital = models.ForeignKey(
        Hospital, on_delete=models.CASCADE, related_name="hospital_reviews", null=True, blank=True)
    ambulance = models.ForeignKey(
        Ambulance, on_delete=models.CASCADE, related_name="ambulance_reviews", null=True, blank=True)
    content = models.TextField(blank=True, null=True)
    rating = models.PositiveIntegerField(default=1)
    created_date = models.DateTimeField(auto_now_add=True)


# Custom signals and methods
@receiver(post_save, sender=Hospital)
@receiver(post_save, sender=AUTH_USER_MODEL)
def create_fund_account(sender, instance, created, **kwargs):
    if created:
        account_number = CustomerAccount.generate_account_number()
        try:
            account = CustomerAccount.objects.get(
                account_number=account_number)
            create_fund_account(sender, instance, created, **kwargs)
        except CustomerAccount.DoesNotExist:
            account_holder = instance
            if isinstance(instance, Hospital):
                account_holder = instance.owner
            account = CustomerAccount.objects.create(
                account_number=account_number, account_holder=account_holder)
            instance.account = account
            instance.save()
