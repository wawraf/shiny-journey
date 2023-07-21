from django.urls import path
from . import views

urlpatterns = [
    path('',  views.index, name='index'),
    path('microservices/<str:microservice>', views.microservices, name='microservices'),
    path('microservices/timestamp/<str:data>', views.timestamp, name='timestamp')
]