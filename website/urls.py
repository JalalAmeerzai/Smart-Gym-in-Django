from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='gym-home'),
    path('classes/', views.classes, name='gym-claases'),
    path('contact/', views.contact, name='gym-contact'),
    path('getregistered/', views.getregistered, name='gym-registration'),
    path('membership/', views.membership, name='gym-membership'),
    path('trainer/', views.trainer, name='gym-trainer'),
    #path('products/<int:myid>', views.products, name='shop-products'),
    #path('checkout/', views.checkout, name='shop-checkout'),
]
