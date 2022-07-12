from django.contrib import admin
from .models import DoctorProfile, DriverProfile, EmergencyContact, PatientProfile, User

# Register your models here.
admin.site.register(User)
admin.site.register(EmergencyContact)
admin.site.register(PatientProfile)
admin.site.register(DoctorProfile)
admin.site.register(DriverProfile)
