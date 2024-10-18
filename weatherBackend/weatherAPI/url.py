from django.urls import path
from .views import get_weatherData

urlpatterns = [
    path('weather/<str:district>/', get_weatherData, name='weather'),
]
