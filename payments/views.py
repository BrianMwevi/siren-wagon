from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def successfull_transaction(request, **kwargs):
    print(request)
    return HttpResponse(request)
