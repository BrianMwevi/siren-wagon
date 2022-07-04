from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

routes = DefaultRouter()
routes.register("packages", views.PackageViewset, basename="packages")
routes.register("trips", views.TripViewset, basename="trips")

urlpatterns = [
    # path('',views.site,name='site'),
    # path('site/<str:pk>/',views.site_id,name='site_id'),
    # path('site-create/',views.siteCreate,name='create'),
    
    
    # path('siteUpdate/<str:id>/',views.siteUpdate,name='update'),
    # path('siteDelete/<str:pk>/',views.siteDelete,name='delete'),
    
    
    
] 

urlpatterns+= routes.urls