from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name="api-login"),
    path('putmeasurements/', views.putmeasurements, name="api-putmeasurements"),
    path('homescreen/', views.homescreen, name="api-homescreen"),
    path('createsuperuser/', views.createsuperuser, name="api-createsuperuser"),
    path('userdiet/', views.userdiet, name="api-userdiet"),
    path('userroutine/', views.userroutine, name="api-userroutine"),
    path('identifymachine/', views.identifymachine, name="api-identifymachine"),
    path('listofroutines/', views.listofroutines, name="api-listofroutines"),
    path('viewroutine/', views.viewroutine, name="api-viewroutine"),
    path('followroutine/', views.followroutine, name="api-followroutine"),
    path('settings/', views.settings, name="api-settings"),
]
