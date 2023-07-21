from django.shortcuts import render
from django.http import JsonResponse
from .MyPackages import Microservices as ms

def index(request):
    return render(request, 'portfolio/index.html')

def timestamp(request, data: str = None):
    if data:
        return JsonResponse(ms.timestamp(data))
    return render(request, "portfolio/microservices/timestamp.html")
