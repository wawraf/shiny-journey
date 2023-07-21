from django.urls import path, include
from . import views


microservices_patterns = [
    path('timestamp/', views.timestamp, name='timestamp'),
    path('timestamp/<str:data>', views.timestamp),
]

urlpatterns = [
    path('',  views.index, name='index'),
    path('microservices/', include(microservices_patterns)),
]
