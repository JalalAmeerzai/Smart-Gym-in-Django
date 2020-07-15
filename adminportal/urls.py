from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name="adminportal-login"),
    path('login/', views.login, name="adminportal-login")
    #path('products/<int:myid>', views.products, name='shop-products'),
    #path('checkout/', views.checkout, name='shop-checkout'),
]
