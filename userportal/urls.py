from django.urls import path
from . import views

urlpatterns = [
    #path('', views.index, name='gym-home'),
    path('login/', views.login, name="userportal-login")
    #path('products/<int:myid>', views.products, name='shop-products'),
    #path('checkout/', views.checkout, name='shop-checkout'),
]
