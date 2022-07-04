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
    
  
  def update(self,serializer):
     serializer.save()
    


# @api_view(['GET'])
# def site(request): 
#   if request.method == 'GET': 
    
#     packages=Package.objects.filter(user=request.user)
#     serializer =PackageSerializer(packages,many=True)
    
#     return Response(serializer.data)
  
  
# @api_view(['GET'])
# def site_id(request,pk): 
#   if request.method == 'GET': 
    
#     packages=Package.objects.filter(id=pk,user=request.user)
#     serializer =PackageSerializer(packages,many=True)
    
#     return Response(serializer.data)


# @api_view(['POST'])
# def siteCreate(request):
#     user = request.user
#     serializer =PackageSerializer(data=request.data)
#     if serializer.is_valid():
#       serializer.save(user=user)
      
#     return Response(serializer.data)
  
  
# @api_view(['PUT'])
# def siteUpdate(request, id):
#     print(id)
  
#     # package_id = request.data.get("id", None)
  
#     # package = Package.objects.get(id=package_id)
    
#     serializer =PackageSerializer(data=request.data)
#     if serializer.is_valid():
#       print("valid")
#       serializer.save()
#     print("Invalid: ", serializer.errors)
      
#     return Response(serializer.data)


# @api_view(['DELETE'])
# def siteDelete(request):
#   user = request.user
#   packages = Package.objects.get()
#   packages = delete =()    

#   return Response('succesfully delete')

