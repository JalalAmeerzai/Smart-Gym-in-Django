from django.shortcuts import render, redirect
from django.http import HttpResponse

def login(request):
    if request.method == 'POST':
        return redirect('/adminportal/dashboard/')
    return render(request, 'adminportal/login.html')



def passwordlost(request):
    return render(request, 'adminportal/lost-password.html')



def dashboard(request):
    return render(request, 'adminportal/dashboard.html')



def settings(request):
    return render(request, 'adminportal/settings.html')



def user(request):
    return render(request, 'adminportal/user.html')



def staff(request):
    return render(request, 'adminportal/staff.html')



def staffprofile(request):
    return render(request, 'adminportal/staffprofile.html')



def staffprofileedit(request):
    return render(request, 'adminportal/editstaff.html')



def trainers(request):
    return render(request, 'adminportal/trainers.html')



def trainersprofile(request):
    return render(request, 'adminportal/trainerprofile.html')



def trainersprofileedit(request):
    return render(request, 'adminportal/edittrainer.html')



def members(request):
    return render(request, 'adminportal/members.html')



def membersprofile(request):
    return render(request, 'adminportal/memberprofile.html')



def membersprofileedit(request):
    return render(request, 'adminportal/editmember.html')



def attendance(request):
    return render(request, 'adminportal/todayattendance.html')



def attendancehistory(request):
    return render(request, 'adminportal/historyattendance.html')



def paymentadd(request):
    return render(request, 'adminportal/addpayment.html')



def paymentdue(request):
    return render(request, 'adminportal/duepayment.html')



def paymenthistory(request):
    return render(request, 'adminportal/historypayment.html')



def paymenthistoryview(request):
    return render(request, 'adminportal/viewhistorypayment.html')



def classes(request):
    return render(request, 'adminportal/classes.html')



def classesedit(request):
    return render(request, 'adminportal/editclass.html')



def expenses(request):
    return render(request, 'adminportal/expenses.html')



def expensesedit(request):
    return render(request, 'adminportal/editexpense.html')



def packages(request):
    return render(request, 'adminportal/packages.html')



def packagesedit(request):
    return render(request, 'adminportal/editpackage.html')



def equipments(request):
    return render(request, 'adminportal/equipments.html')



def equipmentsedit(request):
    return render(request, 'adminportal/editequipments.html')



def exercises(request):
    return render(request, 'adminportal/exercise.html')



def exercisesedit(request):
    return render(request, 'adminportal/editexercise.html')



def routines(request):
    return render(request, 'adminportal/routine.html')



def routinesview(request):
    return render(request, 'adminportal/routineview.html')



def diet(request):
    return render(request, 'adminportal/diet.html')



def dietview(request):
    return render(request, 'adminportal/dietview.html')



def messages(request):
    return render(request, 'adminportal/messagecenter.html')



def messagesreply(request):
    return render(request, 'adminportal/messagereply.html')



def messageswrite(request):
    return render(request, 'adminportal/messagewrite.html')



def messagessent(request):
    return render(request, 'adminportal/messagesent.html')



def messagessentview(request):
    return render(request, 'adminportal/messagesentview.html')



def messagesarchived(request):
    return render(request, 'adminportal/messagearchived.html')



def messagesarchivedview(request):
    return render(request, 'adminportal/messagearchivedview.html')



