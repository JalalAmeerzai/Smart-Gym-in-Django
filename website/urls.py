from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='gym-home'),
    #path('about/', views.about, name='shop-about'),
    #path('contact/', views.contact, name='shop-contact'),
    #path('tracker/', views.tracker, name='shop-tracker'),
    #path('search/', views.search, name='shop-search'),
    #path('products/<int:myid>', views.products, name='shop-products'),
    #path('checkout/', views.checkout, name='shop-checkout'),
]
