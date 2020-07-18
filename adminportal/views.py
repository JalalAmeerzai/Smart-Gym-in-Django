from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import AdminData
from django.utils.datastructures import MultiValueDictKeyError #for files
import base64
import imghdr

def login(request):
    params = {"error": 0, "errormessage": ""} 
    if "userid" in request.session and request.session["userrole"] == "Admin" :
        return redirect('/adminportal/dashboard/')
    else:
        if request.method == 'POST': 
            email = request.POST['email'].lower()
            password = request.POST['password']
            admin = AdminData.objects.filter(admin_password=password, admin_email=email)
            if len(admin) > 0:
                if admin[0].admin_status == "Active":
                    request.session["userid"] = admin[0].admin_id #value to be retrieved from db
                    request.session["userrole"] = admin[0].admin_role #value to be retrived from db
                    request.session["username"] = admin[0].admin_name #value to be retrived from db
                    return redirect('/adminportal/dashboard/')
                else:
                    params["error"] = 1
                    params["errormessage"] ="Your account is deactivated. Contact gym admin."
            else:
                params["error"] = 1
                params["errormessage"] ="Incorrect Email/Password"
        return render(request, 'adminportal/login.html', params)






def logout(request):
    if "userid" in request.session and "userrole" in request.session:
        del request.session["userid"]
        del request.session["userrole"]
        del request.session["username"]
    return redirect('/adminportal/login/')






def passwordlost(request):
    return render(request, 'adminportal/lost-password.html')






def dashboard(request):
    if "userid" in request.session and request.session["userrole"] == "Admin" :
        return render(request, 'adminportal/dashboard.html')
    else:
        return redirect('/adminportal/login/')












def settings(request):
    params = {"imageerror":0, "dataerror":0, "passerror1":0, "passerror2":0}
    if "userid" in request.session and request.session["userrole"] == "Admin" :
        admin = AdminData.objects.filter(admin_id=request.session["userid"])
        params["admin"] = admin[0]
        if request.method == "POST":
            #upload image logic
            if "uploadpicture" in request.POST:
                try:
                    file = request.FILES['picture']
                except MultiValueDictKeyError:
                    file = False
                if file != False:
                    if imghdr.what(file) == None:
                        params["imageerror"] = 1
                    else:
                        image_64_encode = base64.encodebytes(file.read())
                        image_64_decode = base64.decodebytes(image_64_encode)
                        image_result = open("media\\adminportal\\admin\\"+admin[0].admin_img_name, 'wb')
                        image_result.write(image_64_decode)

            #upload data logic
            if "uploaddata" in request.POST:
                name = request.POST["fullname"]
                contact = request.POST["contact"]
                address = request.POST["address"]
                dob = request.POST.get("dob", "")
                status = request.POST.get("status","Active")
                update = AdminData.objects.filter(admin_id=request.session["userid"]).update(admin_name=name, admin_contact=contact, admin_address=address, admin_dob=dob, admin_status=status)
                if update == 0:
                    params["dataerror"] = 1
                else:
                    request.session["username"] = name
            
            #upload data logic
            if "uploadpassword" in request.POST:
                password = request.POST["pass"]
                newpassword = request.POST["newpass"]
                passwordtest = AdminData.objects.filter(admin_id=request.session["userid"], admin_password=password)
                if len(passwordtest) > 0:
                    updatepassword = AdminData.objects.filter(admin_id=request.session["userid"]).update(admin_password=newpassword)
                    if updatepassword == 0:
                        params["passerror2"] = -1 # unsuccessful
                    else:
                        params["passerror2"] = 1 # successful
                else:
                    params["passerror1"] = 1
    
        return render(request, 'adminportal/settings.html', params)
    else:
        return redirect('/adminportal/login/')












def user(request):
    params={}
    if "userid" in request.session and request.session["userrole"] == "Admin" :
        admin = AdminData.objects.filter(admin_id = request.session["userid"])
        params["admin"] = admin[0]
        return render(request, 'adminportal/user.html', params)
    else:
        return redirect('/adminportal/login/')






def staff(request):
    params={}
    if "userid" in request.session and request.session["userrole"] == "Admin" :
        return render(request, 'adminportal/staff.html',params)
    else:
        return redirect('/adminportal/login/')






def staffprofile(request):
    if "userid" in request.session and request.session["userrole"] == "Admin" :
        return render(request, 'adminportal/staffprofile.html')
    else:
        return redirect('/adminportal/login/')






def staffprofileedit(request):
    if "userid" in request.session and request.session["userrole"] == "Admin" :
        if request.method == "POST":
            if "uploadpicture" in request.POST:
                try:
                    file = request.FILES['picture']
                except MultiValueDictKeyError:
                    file = False
                image_64_encode = base64.encodebytes(file.read())
                image_64_decode = base64.decodebytes(image_64_encode)
                image_result = open("media\\adminportal\\admin\\adm1.jpg", 'wb')
                image_result.write(image_64_decode)
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
    



