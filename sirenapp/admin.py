from django.contrib import admin
from .models import CustomerAccount, Trip, Package, Transaction, Hospital, Ambulance

admin.site.register(CustomerAccount)
admin.site.register(Trip)
admin.site.register(Package)
admin.site.register(Transaction)
admin.site.register(Ambulance)
admin.site.register(Hospital)
