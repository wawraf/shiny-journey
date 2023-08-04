from django.urls import path
from . import views

app_name = 'steganography'

urlpatterns = [
    path('steganography/',  views.index, name='index')
]