from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name="api-login"),
    path('putmeasurements/', views.putmeasurements, name="api-putmeasurements"),
    path('homescreen/', views.homescreen, name="api-homescreen")
]
