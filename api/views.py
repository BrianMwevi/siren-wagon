from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework import viewsets

from sirenapp.models import Package,Trip
from .serializers import PackageSerializer,TripSerializer


# Create your views here.

class PackageViewset(viewsets.ModelViewSet):
  serializer_class = PackageSerializer
  queryset = Package.objects.all()
  
  def perform_create(self, serializer):
    serializer.save(user=self.request.user)
    

class TripViewset(viewsets.ModelViewSet):
  serializer_class = TripSerializer
  queryset = Trip.objects.all()
  
  def perform_create(self, serializer):
    serializer.save(driver=self.request.user)
    
  
  


