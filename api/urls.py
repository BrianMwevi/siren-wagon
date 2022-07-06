from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from api.views import AmbulanceViewset, DriverViewset, EmergencyContactViewset, HospitalViewset, TransactionsView, TripViewset, ReviewViewset, DoctorViewset, PackageViewset, PatientProfileView, UserRegisterView, LogoutView

from django.urls import path


router = DefaultRouter()

router.register('hospitals', HospitalViewset, basename='hospitals')
router.register('trips', TripViewset, basename='trips')
router.register('reviews', ReviewViewset, basename='reviews')
router.register('doctors', DoctorViewset, basename='doctors')
router.register('ambulances', AmbulanceViewset, basename='ambulances')
router.register('drivers', DriverViewset, basename='drivers')
router.register('packages', PackageViewset, basename='packages')
router.register('emergencies', EmergencyContactViewset, basename='emergencies')

urlpatterns = [
    path('transactions/', TransactionsView.as_view(), name='transactions'),
    path('patients/', PatientProfileView.as_view(), name='patients-list'),
    path('patients/<int:id>/', PatientProfileView.as_view(), name='patients-detail'),
    path('users/register/', UserRegisterView.as_view(), name='register'),
    path('users/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/logout/', LogoutView.as_view(), name='auth_logout'),

]
urlpatterns += router.urls
