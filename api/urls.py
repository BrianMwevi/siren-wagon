from rest_framework.routers import DefaultRouter
from api.views import AmbulanceViewset, AppUserViewset, DriverViewset, HospitalViewset, TransactionsView, TripViewset, ReviewViewset, DoctorViewset
from django.urls import path


router = DefaultRouter()
# router.register('transactions', TransactionsView, basename='transactions')
router.register('users', AppUserViewset, basename='users')
router.register('hospitals', HospitalViewset, basename='hospitals')
router.register('trips', TripViewset, basename='trips')
router.register('reviews', ReviewViewset, basename='review')
router.register('doctors', DoctorViewset, basename='doctor')
router.register('ambulances', AmbulanceViewset, basename='ambulance')
router.register('drivers', DriverViewset, basename='driver')

urlpatterns = [
    path('transactions/', TransactionsView.as_view(), name='transactions'),

]

urlpatterns += router.urls
