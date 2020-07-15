from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name="userportal-login"),
    path('login/', views.login, name="userportal-login"),
    path('passwordlost/', views.passwordlost, name="userportal-passwordlost"),
    path('user/', views.userprofile, name="userportal-userprofile"),
    path('settings/', views.settings, name="userportal-settings"),
    path('routines/', views.routines, name="userportal-routines"),
    path('createroutine/', views.createroutines, name="userportal-createroutines"),
    path('viewroutine/', views.viewroutine, name="userportal-viewroutine"),
    path('diet/', views.diet, name="userportal-diet"),
    path('exercises/', views.exercises, name="userportal-exercises"),
    path('finances/', views.finances, name="userportal-finances"),
    path('help/', views.help, name="userportal-help"),
    path('subscription/', views.subscription, name="userportal-subscription"),
    #path('products/<int:myid>', views.products, name='shop-products'),
    #path('checkout/', views.checkout, name='shop-checkout'),
]
