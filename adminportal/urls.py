from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name="adminportal-login"),
    path('login/', views.login, name="adminportal-login"),
    path('logout/', views.logout, name="adminportal-logout"),
    path('passwordlost/', views.passwordlost, name="adminportal-passwordlost"),
    path('dashboard/', views.dashboard, name="adminportal-dashboard"),
    path('settings/', views.settings, name="adminportal-settings"),
    path('user/', views.user, name="adminportal-user"),
    path('staff/', views.staff, name="adminportal-staff"),
    path('staffprofile/<str:adminid>', views.staffprofile, name="adminportal-staffprofile"),
    path('staffprofileedit/<str:adminid>', views.staffprofileedit, name="adminportal-staffprofileedit"),
    path('trainers/', views.trainers, name="adminportal-trainers"),
    path('trainersprofile/<str:trainerid>', views.trainersprofile, name="adminportal-trainersprofile"),
    path('trainersprofileedit/<str:trainerid>', views.trainersprofileedit, name="adminportal-trainersprofileedit"),
    path('members/', views.members, name="adminportal-members"),
    path('membersprofile/<str:memid>', views.membersprofile, name="adminportal-membersprofile"),
    path('membersprofileedit/<str:memid>', views.membersprofileedit, name="adminportal-membersprofileedit"),
    path('attendance/', views.attendance, name="adminportal-attendance"),
    path('attendancehistory/', views.attendancehistory, name="adminportal-attendancehistory"),
    path('paymentadd/<str:memid>', views.paymentadd, name="adminportal-paymentadd"),
    path('paymentdue/', views.paymentdue, name="adminportal-paymentdue"),
    path('paymenthistory/', views.paymenthistory, name="adminportal-paymenthistory"),
    path('paymenthistoryview/<str:memid>', views.paymenthistoryview, name="adminportal-paymenthistoryview"),
    path('classes/', views.classes, name="adminportal-classes"),
    path('classesedit/<str:classid>', views.classesedit, name="adminportal-classesedit"),
    path('expenses/', views.expenses, name="adminportal-expenses"),
    path('expensesedit/<str:expid>', views.expensesedit, name="adminportal-expensesedit"),
    path('packages/', views.packages, name="adminportal-packages"),
    path('packagesedit/<str:pkgid>', views.packagesedit, name="adminportal-packagesedit"),
    path('equipments/', views.equipments, name="adminportal-equipments"),
    path('equipmentsedit/<str:eqid>', views.equipmentsedit, name="adminportal-equipmentsedit"),
    path('exercises/', views.exercises, name="adminportal-exercises"),
    path('exercisesedit/<str:exrid>', views.exercisesedit, name="adminportal-exercisesedit"),
    path('routines/', views.routines, name="adminportal-routines"),
    path('routinesview/<str:rtid>', views.routinesview, name="adminportal-routinesview"),
    path('diet/', views.diet, name="adminportal-diet"),
    path('dietview/<str:dtid>', views.dietview, name="adminportal-dietview"),
    path('messages/', views.messages, name="adminportal-messages"),
    path('messagesreply/<int:msgid>', views.messagesreply, name="adminportal-messagesreply"),
    path('messageswrite/', views.messageswrite, name="adminportal-messageswrite"),
    path('messagessent/', views.messagessent, name="adminportal-messagessent"),
    path('messagessentview/<int:msgid>', views.messagessentview, name="adminportal-messagessentview"),
    path('messagesarchived/', views.messagesarchived, name="adminportal-messagesarchived"),
    path('messagesarchivedview/<int:msgid>', views.messagesarchivedview, name="adminportal-messagesarchivedview"),
    #path('products/<int:myid>', views.products, name='shop-products'),
    #path('checkout/', views.checkout, name='shop-checkout'),
]
