from django.urls import path, include
from . import views


microservices_patterns = [
    path('timestamp/', views.timestamp, name='timestamp'),
    path('timestamp/<str:data>', views.timestamp),
    path('header/', views.header, name='header'),
    path('header/<str:data>', views.header),
    path('file/', views.metadata, name='file')
]

urlpatterns = [
    path('',  views.index, name='index'),
    path('microservices/', include(microservices_patterns)),
]
