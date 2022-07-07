from django.contrib import admin
from .models import CustomerAccount, Trip, Package, Transaction, Hospital, Driver, Doctor, Ambulance

admin.site.register(CustomerAccount)
admin.site.register(Trip)
admin.site.register(Package)
admin.site.register(Transaction)
admin.site.register(Doctor)
admin.site.register(Ambulance)
admin.site.register(Driver)
admin.site.register(Hospital)
