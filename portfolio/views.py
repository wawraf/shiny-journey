from django.shortcuts import render
from django.http import JsonResponse
from .MyPackages import Microservices as ms

def index(request):
    return render(request, 'portfolio/index.html')

def microservices(request, microservice: str):
    if microservice == "timestamp":
        return render(request, "portfolio/microservices/timestamp.html")

    return render(request, 'portfolio/index.html')

def timestamp(request, data: str):
    return JsonResponse(ms.timestamp(data))