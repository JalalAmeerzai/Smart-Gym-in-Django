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
    path('attendance/', views.attendance, name="adminportal-attendance"),
    path('attendancehistory/', views.attendancehistory, name="adminportal-attendancehistory"),
    path('paymentadd/', views.paymentadd, name="adminportal-paymentadd"),
    path('paymentdue/', views.paymentdue, name="adminportal-paymentdue"),
    path('paymenthistory/', views.paymenthistory, name="adminportal-paymenthistory"),
    path('paymenthistoryview/', views.paymenthistoryview, name="adminportal-paymenthistoryview"),
    path('classes/', views.classes, name="adminportal-classes"),
    path('classesedit/', views.classesedit, name="adminportal-classesedit"),
    path('expenses/', views.expenses, name="adminportal-expenses"),
    path('expensesedit/', views.expensesedit, name="adminportal-expensesedit"),
    path('packages/', views.packages, name="adminportal-packages"),
    path('packagesedit/', views.packagesedit, name="adminportal-packagesedit"),
    path('equipments/', views.equipments, name="adminportal-equipments"),
    path('equipmentsedit/', views.equipmentsedit, name="adminportal-equipmentsedit"),
    path('exercises/', views.exercises, name="adminportal-exercises"),
    path('exercisesedit/', views.exercisesedit, name="adminportal-exercisesedit"),
    path('routines/', views.routines, name="adminportal-routines"),
    path('routinesview/', views.routinesview, name="adminportal-routinesview"),
    path('diet/', views.diet, name="adminportal-diet"),
    path('dietview/', views.dietview, name="adminportal-dietview"),
    path('messages/', views.messages, name="adminportal-messages"),
    path('messagesreply/', views.messagesreply, name="adminportal-messagesreply"),
    path('messageswrite/', views.messageswrite, name="adminportal-messageswrite"),
    path('messagessent/', views.messagessent, name="adminportal-messagessent"),
    path('messagessentview/', views.messagessentview, name="adminportal-messagessentview"),
    path('messagesarchived/', views.messagesarchived, name="adminportal-messagesarchived"),
    path('messagesarchivedview/', views.messagesarchivedview, name="adminportal-messagesarchivedview"),
    #path('products/<int:myid>', views.products, name='shop-products'),
    #path('checkout/', views.checkout, name='shop-checkout'),
]
