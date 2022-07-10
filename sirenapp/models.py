from django.db import models
from core.settings import AUTH_USER_MODEL as User
from django.dispatch import receiver
from django.db.models.signals import post_save


class Hospital(models.Model):
    name = models.CharField(max_length=255, unique=True)
    location = models.CharField(max_length=255)
    patients = models.ManyToManyField(
        User, related_name='hospital_patients', blank=True)
    ambulances = models.ManyToManyField(
        'Ambulance', related_name='hospital_ambulances', blank=True)
    established_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    doctors = models.ManyToManyField(
        'Doctor', related_name='hospital_doctors', blank=True)
    reviews = models.ManyToManyField(
        'Review', related_name='hospital_reviews', blank=True)
    account = models.ForeignKey(
        'CustomerAccount', related_name='hospital_account', blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Ambulance(models.Model):
    driver = models.ForeignKey(
        'Driver', on_delete=models.SET_NULL, null=True, related_name='driver', blank=True)
    number_plate = models.CharField(max_length=200, blank=True, null=True)
    available = models.BooleanField('available', default=False)
    trips = models.ManyToManyField(
        'Trip', blank=True, related_name='ambulance_trips')
    ratings = models.ManyToManyField(
        'Review', blank=True, related_name='ratings')

    def __str__(self):
        return self.number_plate


class Doctor(models.Model):
    first_name = models.CharField(max_length=55)
    last_name = models.CharField(max_length=55)
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=255)
    ambulance = models.ForeignKey(
        Ambulance, on_delete=models.CASCADE, related_name="ambulance_doctor",null=True)


class Driver(models.Model):
    first_name = models.CharField(max_length=55)
    last_name = models.CharField(max_length=55)
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=255)
    trips = models.ManyToManyField('Trip', blank=True, related_name='trips')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class CustomerAccount(models.Model):
    account_holder = models.ForeignKey(
        User, related_name='customer_account', on_delete=models.CASCADE, null=True, blank=True)
    hospital = models.ForeignKey(
        Hospital, related_name='hospital_account', on_delete=models.CASCADE, null=True, blank=True)
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

    @classmethod
    def get_account(cls, account_number):
        account = cls.objects.get(account_number=account_number)
        return account

     # Deposit to one's account
    @classmethod
    def deposit(cls, sender, amount):
        account = cls.objects.get(account_holder=sender)
        account.balance += amount
        account.save()
        return account.balance

    @ classmethod
    def withdraw(cls, sender, amount):
        account = cls.objects.get(account_holder=sender)
        account.balance -= amount
        account.save()
        return account.balance

    @ classmethod
    def transfer(cls, sender, account_number, amount):
        sender_account = cls.objects.get(account_holder=sender)
        receiver_account = cls.objects.get(account_number=account_number)
        sender_account.balance -= amount
        receiver_account.balance += amount
        sender_account.save()
        receiver_account.save()
        return sender_account.balance

    @classmethod
    def can_transact(cls, account_number, amount):
        account = cls.get_account(account_number)
        print(account.balance, amount)
        return account.balance >= amount

    def __str__(self):
        if self.account_holder:
            return f"{self.account_holder.username}: {self.account_number}"
        return f"{self.hospital.name}: {self.account_number}"


class Transaction(models.Model):
    sender = models.ForeignKey(
        User, related_name='sender', on_delete=models.CASCADE, null=True, blank=True)
    receiver = models.ForeignKey(
        CustomerAccount, related_name='receiver', on_delete=models.CASCADE,null=True, blank=True)
    amount = models.PositiveIntegerField(default=0)
    transaction_type = models.CharField(max_length=55)
    completed = models.BooleanField(default=False)
    transaction_date = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     if self.receiver.account_holder:
    #         return f"{self.transaction_type.title()}: {self.sender.username.title()} TO {self.receiver.account_holder.username.title()}"
    #     else:
    #         return f"{self.transaction_type.title()}: {self.sender.username.title()} TO {self.receiver.hospital.name.title()}"


class Package(models.Model):
    CHOICES = [
        ('1', 'Regular'),
        ('2', 'Premium'),
    ]
    package_choice = models.CharField(
        max_length=200, choices=CHOICES, default="regular")
    amount = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.package_choice


class Trip(models.Model):
    pickup = models.CharField(max_length=255)
    destination = models.ForeignKey(
        Hospital, on_delete=models.CASCADE, related_name="trips", null=True, blank=True)
    persons = models.PositiveIntegerField(default=3)
    fee = models.ForeignKey(
        'Transaction', related_name='trip_fee', on_delete=models.CASCADE, blank=True, null=True)
    trip_date = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    def calculate_fees(self):
        """A method to calculate the transportation charges between the pickup point and the hospital"""
        pass

    def __str__(self):
        return f"{self.pickup} TO {self.destination}"


class Review(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reviewer")
    hospital = models.ForeignKey(
        Hospital, on_delete=models.CASCADE, related_name="hospital_reviews", null=True, blank=True)
    ambulance = models.ForeignKey(
        Ambulance, on_delete=models.CASCADE, related_name="ambulance_reviews", null=True, blank=True)
    content = models.TextField(blank=True, null=True)
    rating = models.PositiveIntegerField(default=1)
    created_date = models.DateTimeField(auto_now_add=True)


# Custom signals and methods
@receiver(post_save, sender=Transaction)
def update_account_balance(sender, instance, created, **kwargs):
    if created:
        instance.completed = True
        instance.save()
        transaction = instance.transaction_type.lower()
        if transaction == "deposit":
            return CustomerAccount.deposit(instance.sender, instance.amount)
        if transaction == "withdraw":
            return CustomerAccount.withdraw(instance.sender, instance.amount)
        if transaction == "transfer":
            account_number = instance.receiver.account_number
            return CustomerAccount.transfer(instance.sender, account_number, instance.amount)


@receiver(post_save, sender=Hospital)
@receiver(post_save, sender=User)
def create_fund_account(sender, instance, created, **kwargs):
    if created:
        account_number = CustomerAccount.generate_account_number()
        try:
            account = CustomerAccount.objects.get(
                account_number=account_number)
            return create_fund_account(sender, instance, created, **kwargs)
        except CustomerAccount.DoesNotExist:
            account = None
            if isinstance(instance, Hospital):
                account = CustomerAccount.objects.create(
                    account_number=account_number, hospital=instance)
            else:
                account = CustomerAccount.objects.create(
                    account_number=account_number, account_holder=instance)
            instance.account = account
            instance.save()