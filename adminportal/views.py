from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import AdminData, TrainerData
from django.utils.datastructures import MultiValueDictKeyError #for files
import base64
import imghdr
import datetime
import os

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
            
            #upload password logic
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

        #main page logic
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
    params={"error":0, "errormessage":"", "success":0, "successmessage":""}
    admin_count = AdminData.objects.all().order_by('admin_id')
    
    if "userid" in request.session and request.session["userrole"] == "Admin" :

        # add admin logic
        if "addadmin" in request.POST:
            new_id = "adm" + str((int(admin_count[len(admin_count)-1].admin_id[-1])+1))
            try:
                file = request.FILES['picture']
            except MultiValueDictKeyError:
                file = False
            if file != False:
                if imghdr.what(file) == None:
                    params["error"] = 1
                    params["errormessage"] = "Select a suitable image file type"
                else:
                    email = request.POST["email"].lower()
                    if admin_count.filter(admin_email=email).exists():
                        params["error"] = 1
                        params["errormessage"] = "Account with email address '"+email+"' already exists!"
                    else:
                        try:
                            name = request.POST["name"]
                            password = request.POST["password"]
                            contact = request.POST["contact"]
                            address = request.POST["address"]
                            dob = request.POST.get("dob","")
                            status = request.POST.get("status","Active")
                            added_by = request.session["userid"]
                            added_on = datetime.datetime.now().strftime("%Y-%m-%d")
                            picture = new_id+".jpg"
                            new_admin = AdminData(admin_id=new_id, admin_name=name, admin_email=email, admin_password=password, admin_contact=contact, admin_address=address, admin_dob=dob, admin_status=status, admin_role="Admin", admin_img_name=picture, admin_added_by=added_by, admin_added_on=added_on)
                            new_admin.save()
                            image_64_encode = base64.encodebytes(file.read())
                            image_64_decode = base64.decodebytes(image_64_encode)
                            image_result = open("media\\adminportal\\admin\\"+picture, 'wb')
                            image_result.write(image_64_decode)
                            params["success"] = 1
                            params["successmessage"] = "Staff member added successfully."
                        except Exception:
                            params["error"] = 1
                            params["errormessage"] = "Something went wrong. Try again later."

        # delete admin logic
        if "deleteadmin" in request.POST:
            del_id = request.POST["id"]
            admin_delete = AdminData.objects.filter(admin_id = del_id).delete()
            if admin_delete[0] == 1:
                try:
                    os.remove("media\\adminportal\\admin\\"+del_id+".jpg")
                    params["success"] = 1
                    params["successmessage"] = "Staff member successfully deleted."
                except Exception:
                    pass
            else:
                params["error"] = 1
                params["errormessage"] = "Something went wrong. Try again later."

        #main page logic
        params["admins"] = admin_count
        return render(request, 'adminportal/staff.html',params)
    else:
        return redirect('/adminportal/login/')












def staffprofile(request, adminid):
    params={}
    if "userid" in request.session and request.session["userrole"] == "Admin" :
        admin = AdminData.objects.filter(admin_id = adminid)
        params["admin"] = admin[0]
        return render(request, 'adminportal/staffprofile.html',params)
    else:
        return redirect('/adminportal/login/')






def staffprofileedit(request, adminid):
    params = {"imageerror":0, "dataerror":0}
    if "userid" in request.session and request.session["userrole"] == "Admin" :
        admin = AdminData.objects.filter(admin_id=adminid)

        if admin[0].admin_added_by == "superuser":
            return redirect('/adminportal/staff/')

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
                update = AdminData.objects.filter(admin_id=adminid).update(admin_name=name, admin_contact=contact, admin_address=address, admin_dob=dob, admin_status=status)
                if update == 0:
                    params["dataerror"] = 1
        
        params["admin"] = admin[0]
        return render(request, 'adminportal/editstaff.html', params)
    else:
        return redirect('/adminportal/login/')






def trainers(request):
    if "userid" in request.session and request.session["userrole"] == "Admin" :
        params={"error":0, "errormessage":"", "success":0, "successmessage":""}
        trainer_count = TrainerData.objects.all().order_by('trainer_id')

        # add trainer logic
        if "addtrainer" in request.POST:
            if len(trainer_count) == 0:
                new_id = "tr1"
            else:
                new_id = "tr" + str((int(trainer_count[len(trainer_count)-1].trainer_id[-1])+1))

            try:
                file = request.FILES['picture']
            except MultiValueDictKeyError:
                file = False
            if file != False:
                if imghdr.what(file) == None:
                    params["error"] = 1
                    params["errormessage"] = "Select a suitable image file type"
                else:
                    email = request.POST["email"].lower()
                    if trainer_count.filter(trainer_email=email).exists():
                        params["error"] = 1
                        params["errormessage"] = "Account with email address '"+email+"' already exists!"
                    else:
                        try:
                            name = request.POST["name"]
                            about = request.POST["about"]
                            contact = request.POST["contact"]
                            address = request.POST["address"]
                            dob = request.POST.get("dob","")
                            status = request.POST.get("status","Active")
                            height = request.POST["height1"]+"' "+request.POST["height2"]+"''"
                            weight = request.POST["weight"]
                            fb = request.POST["fb"]
                            ig = request.POST["ig"]
                            added_by = request.session["userid"]
                            added_on = datetime.datetime.now().strftime("%Y-%m-%d")
                            picture = new_id+".jpg"
                            new_trainer = TrainerData(trainer_id=new_id, trainer_name=name, trainer_email=email, trainer_about=about, trainer_img_name=picture, trainer_contact=contact, trainer_address=address, trainer_dob=dob, trainer_height=height, trainer_weight=weight, trainer_fb=fb, trainer_ig=ig, trainer_status=status, trainer_added_by=added_by, trainer_added_on=added_on)
                            new_trainer.save()
                            image_64_encode = base64.encodebytes(file.read())
                            image_64_decode = base64.decodebytes(image_64_encode)
                            image_result = open("media\\adminportal\\trainer\\"+picture, 'wb')
                            image_result.write(image_64_decode)
                            params["success"] = 1
                            params["successmessage"] = "Trainer added successfully."
                        except Exception:
                            params["error"] = 1
                            params["errormessage"] = "Something went wrong. Try again later."

        # delete trainer logic
        if "deletetrainer" in request.POST:
            del_id = request.POST["id"]
            trainer_delete = TrainerData.objects.filter(trainer_id = del_id).delete()
            if trainer_delete[0] == 1:
                try:
                    os.remove("media\\adminportal\\trainer\\"+del_id+".jpg")
                    params["success"] = 1
                    params["successmessage"] = "Trainer successfully deleted."
                except Exception:
                    pass
            else:
                params["error"] = 1
                params["errormessage"] = "Something went wrong. Try again later."


        params["trainers"] = trainer_count
        return render(request, 'adminportal/trainers.html', params)
    else:
        return redirect('/adminportal/login/')






def trainersprofile(request, trainerid):
    params={}
    if "userid" in request.session and request.session["userrole"] == "Admin" :
        trainer = TrainerData.objects.filter(trainer_id = trainerid)
        params["trainer"] = trainer[0]
        return render(request, 'adminportal/trainerprofile.html', params)
    else:
        return redirect('/adminportal/login/')
    





def trainersprofileedit(request, trainerid):
    params = {"imageerror":0, "dataerror":0}
    if "userid" in request.session and request.session["userrole"] == "Admin" :
        trainer = TrainerData.objects.filter(trainer_id = trainerid)

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
                        image_result = open("media\\adminportal\\trainer\\"+trainer[0].trainer_img_name, 'wb')
                        image_result.write(image_64_decode)
            
            #upload data logic
            if "uploaddata" in request.POST:
                name = request.POST["name"]
                about = request.POST.get("about","")
                contact = request.POST["contact"]
                address = request.POST["address"]
                dob = request.POST.get("dob","")
                status = request.POST.get("status","Active")
                height = request.POST["height1"]+"' "+request.POST["height2"]+"''"
                weight = request.POST["weight"]
                fb = request.POST["fb"]
                ig = request.POST["ig"]
                update = TrainerData.objects.filter(trainer_id=trainerid).update(trainer_name=name, trainer_contact=contact, trainer_about=about, trainer_height=height, trainer_weight=weight, trainer_fb= fb, trainer_ig= ig, trainer_address=address, trainer_dob=dob, trainer_status=status)
                if update == 0:
                    params["dataerror"] = 1


        params["trainer"] = trainer[0]
        return render(request, 'adminportal/edittrainer.html', params)
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
    



