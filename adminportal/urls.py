from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name="adminportal-login"),
    path('login/', views.login, name="adminportal-login"),
    path('passwordlost/', views.passwordlost, name="adminportal-passwordlost"),
    path('dashboard/', views.dashboard, name="adminportal-dashboard"),
    path('settings/', views.settings, name="adminportal-settings"),
    path('user/', views.user, name="adminportal-user"),
    path('staff/', views.staff, name="adminportal-staff"),
    path('staffprofile/', views.staffprofile, name="adminportal-staffprofile"),
    path('staffprofileedit/', views.staffprofileedit, name="adminportal-staffprofileedit"),
    path('trainers/', views.trainers, name="adminportal-trainers"),
    path('trainersprofile/', views.trainersprofile, name="adminportal-trainersprofile"),
    path('trainersprofileedit/', views.trainersprofileedit, name="adminportal-trainersprofileedit"),
    path('members/', views.members, name="adminportal-members"),
    path('membersprofile/', views.membersprofile, name="adminportal-membersprofile"),
    path('membersprofileedit/', views.membersprofileedit, name="adminportal-membersprofileedit"),
    #path('products/<int:myid>', views.products, name='shop-products'),
    #path('checkout/', views.checkout, name='shop-checkout'),
]
