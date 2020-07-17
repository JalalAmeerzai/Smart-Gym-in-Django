from django.shortcuts import render, redirect
from django.http import HttpResponse

def login(request):
    if "userid" in request.session and request.session["userrole"] == "Admin" :
        return redirect('/adminportal/dashboard/')
    else:
        if request.method == 'POST': 
            email = request.POST['email']
            password = request.POST['password']
            request.session["userid"] = "adm1" #value to be retrieved from db
            request.session["userrole"] = "Admin" #value to be retrived from db
            print("session created")
            return redirect('/adminportal/dashboard/')
        else:
            return render(request, 'adminportal/login.html')






def logout(request):
    if "userid" in request.session and "userrole" in request.session:
        del request.session["userid"]
        del request.session["userrole"]
    return redirect('/adminportal/login/')






def passwordlost(request):
    return render(request, 'adminportal/lost-password.html')






def dashboard(request):
    if "userid" in request.session and request.session["userrole"] == "Admin" :
        return render(request, 'adminportal/dashboard.html')
    else:
        return redirect('/adminportal/login/')






def settings(request):
    if "userid" in request.session and request.session["userrole"] == "Admin" :
        return render(request, 'adminportal/settings.html')
    else:
        return redirect('/adminportal/login/')






def user(request):
    if "userid" in request.session and request.session["userrole"] == "Admin" :
        return render(request, 'adminportal/user.html')
    else:
        return redirect('/adminportal/login/')






def staff(request):
    if "userid" in request.session and request.session["userrole"] == "Admin" :
        return render(request, 'adminportal/staff.html')
    else:
        return redirect('/adminportal/login/')






def staffprofile(request):
    if "userid" in request.session and request.session["userrole"] == "Admin" :
        return render(request, 'adminportal/staffprofile.html')
    else:
        return redirect('/adminportal/login/')






def staffprofileedit(request):
    if "userid" in request.session and request.session["userrole"] == "Admin" :
        return render(request, 'adminportal/editstaff.html')
    else:
        return redirect('/adminportal/login/')






def trainers(request):
    if "userid" in request.session and request.session["userrole"] == "Admin" :
        return render(request, 'adminportal/trainers.html')
    else:
        return redirect('/adminportal/login/')






def trainersprofile(request):
    if "userid" in request.session and request.session["userrole"] == "Admin" :
        return render(request, 'adminportal/trainerprofile.html')
    else:
        return redirect('/adminportal/login/')
    





def trainersprofileedit(request):
    if "userid" in request.session and request.session["userrole"] == "Admin" :
        return render(request, 'adminportal/edittrainer.html')
    else:
        return redirect('/adminportal/login/')
    





def members(request):
    if "userid" in request.session and request.session["userrole"] == "Admin" :
        return render(request, 'adminportal/members.html')
    else:
        return redirect('/adminportal/login/')
    





def membersprofile(request):
    if "userid" in request.session and request.session["userrole"] == "Admin" :
        return render(request, 'adminportal/memberprofile.html')
    else:
        return redirect('/adminportal/login/')
    





def membersprofileedit(request):
    if "userid" in request.session and request.session["userrole"] == "Admin" :
        return render(request, 'adminportal/editmember.html')
    else:
        return redirect('/adminportal/login/')
    





def attendance(request):
    if "userid" in request.session and request.session["userrole"] == "Admin" :
        return render(request, 'adminportal/todayattendance.html')
    else:
        return redirect('/adminportal/login/')
    





def attendancehistory(request):
    if "userid" in request.session and request.session["userrole"] == "Admin" :
        return render(request, 'adminportal/historyattendance.html')
    else:
        return redirect('/adminportal/login/')
    





def paymentadd(request):
    if "userid" in request.session and request.session["userrole"] == "Admin" :
        return render(request, 'adminportal/addpayment.html')
    else:
        return redirect('/adminportal/login/')
    





def paymentdue(request):
    if "userid" in request.session and request.session["userrole"] == "Admin" :
        return render(request, 'adminportal/duepayment.html')
    else:
        return redirect('/adminportal/login/')
    





def paymenthistory(request):
    if "userid" in request.session and request.session["userrole"] == "Admin" :
        return render(request, 'adminportal/historypayment.html')
    else:
        return redirect('/adminportal/login/')
    





def paymenthistoryview(request):
    if "userid" in request.session and request.session["userrole"] == "Admin" :
         return render(request, 'adminportal/viewhistorypayment.html')
    else:
        return redirect('/adminportal/login/')
   





def classes(request):
    if "userid" in request.session and request.session["userrole"] == "Admin" :
         return render(request, 'adminportal/classes.html')
    else:
        return redirect('/adminportal/login/')
    





def classesedit(request):
    if "userid" in request.session and request.session["userrole"] == "Admin" :
         return render(request, 'adminportal/editclass.html')
    else:
        return redirect('/adminportal/login/')
    





def expenses(request):
    if "userid" in request.session and request.session["userrole"] == "Admin" :
         return render(request, 'adminportal/expenses.html')
    else:
        return redirect('/adminportal/login/')
    





def expensesedit(request):
    if "userid" in request.session and request.session["userrole"] == "Admin" :
         return render(request, 'adminportal/editexpense.html')
    else:
        return redirect('/adminportal/login/')
    





def packages(request):
    if "userid" in request.session and request.session["userrole"] == "Admin" :
         return render(request, 'adminportal/packages.html')
    else:
        return redirect('/adminportal/login/')
    





def packagesedit(request):
    if "userid" in request.session and request.session["userrole"] == "Admin" :
         return render(request, 'adminportal/editpackage.html')
    else:
        return redirect('/adminportal/login/')
    





def equipments(request):
    if "userid" in request.session and request.session["userrole"] == "Admin" :
         return render(request, 'adminportal/equipments.html')
    else:
        return redirect('/adminportal/login/')
    





def equipmentsedit(request):
    if "userid" in request.session and request.session["userrole"] == "Admin" :
         return render(request, 'adminportal/editequipments.html')
    else:
        return redirect('/adminportal/login/')
    





def exercises(request):
    if "userid" in request.session and request.session["userrole"] == "Admin" :
         return render(request, 'adminportal/exercise.html')
    else:
        return redirect('/adminportal/login/')
    





def exercisesedit(request):
    if "userid" in request.session and request.session["userrole"] == "Admin" :
         return render(request, 'adminportal/editexercise.html')
    else:
        return redirect('/adminportal/login/')
    





def routines(request):
    if "userid" in request.session and request.session["userrole"] == "Admin" :
         return render(request, 'adminportal/routine.html')
    else:
        return redirect('/adminportal/login/')
    





def routinesview(request):
    if "userid" in request.session and request.session["userrole"] == "Admin" :
         return render(request, 'adminportal/routineview.html')
    else:
        return redirect('/adminportal/login/')
    





def diet(request):
    if "userid" in request.session and request.session["userrole"] == "Admin" :
         return render(request, 'adminportal/diet.html')
    else:
        return redirect('/adminportal/login/')
    





def dietview(request):
    if "userid" in request.session and request.session["userrole"] == "Admin" :
         return render(request, 'adminportal/dietview.html')
    else:
        return redirect('/adminportal/login/')
    





def messages(request):
    if "userid" in request.session and request.session["userrole"] == "Admin" :
         return render(request, 'adminportal/messagecenter.html')
    else:
        return redirect('/adminportal/login/')
    





def messagesreply(request):
    if "userid" in request.session and request.session["userrole"] == "Admin" :
         return render(request, 'adminportal/messagereply.html')
    else:
        return redirect('/adminportal/login/')
    





def messageswrite(request):
    if "userid" in request.session and request.session["userrole"] == "Admin" :
         return render(request, 'adminportal/messagewrite.html')
    else:
        return redirect('/adminportal/login/')
    





def messagessent(request):
    if "userid" in request.session and request.session["userrole"] == "Admin" :
         return render(request, 'adminportal/messagesent.html')
    else:
        return redirect('/adminportal/login/')
    





def messagessentview(request):
    if "userid" in request.session and request.session["userrole"] == "Admin" :
         return render(request, 'adminportal/messagesentview.html')
    else:
        return redirect('/adminportal/login/')
    





def messagesarchived(request):
    if "userid" in request.session and request.session["userrole"] == "Admin" :
         return render(request, 'adminportal/messagearchived.html')
    else:
        return redirect('/adminportal/login/')
    





def messagesarchivedview(request):
    if "userid" in request.session and request.session["userrole"] == "Admin" :
         return render(request, 'adminportal/messagearchivedview.html')
    else:
        return redirect('/adminportal/login/')
    



