from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import AdminData, TrainerData, PackageData, EquipmentData, ClassData, ExpenseData, ExerciseData, DietData
from django.utils.datastructures import MultiValueDictKeyError #for files
import base64
import imghdr
import datetime
import os
import re #regex
from django.core.mail import send_mail
import json 




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
        return render(request, 'adminportal/dashboard.html',{"users":{"active": 100, "inactive": 2},"data":[4000, 6000, 8000, 10000, 14000, 20000, 12500]})
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
                        return redirect('/adminportal/user/')

            #upload data logic
            if "uploaddata" in request.POST:
                name = request.POST["fullname"].title()
                contact = request.POST["contact"]
                address = request.POST["address"]
                dob = request.POST.get("dob", "")
                status = request.POST.get("status","Active")
                update = AdminData.objects.filter(admin_id=request.session["userid"]).update(admin_name=name, admin_contact=contact, admin_address=address, admin_dob=dob, admin_status=status)
                if update == 0:
                    params["dataerror"] = 1
                else:
                    request.session["username"] = name
                    return redirect('/adminportal/user/')
            
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
        admin = AdminData.objects.filter(admin_id=request.session["userid"])
        params["admin"] = admin[0]
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
                            name = request.POST["name"].title()
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
                            try:
                                send_mail(
                                    'Welcome to SmartGym - This Email Contains your Account Credentials',
                                    '\nHello '+name+',\nYour account credenatials for smartgym are: \nAccount: '+email+'\nPassword: '+password+"\n\nStay Fit.\n\n\nRegards\n"+request.session["username"]+"\n"+request.session["userid"],
                                    'SmartGym',
                                    [email], 
                                )
                                params["success"] = 1
                                params["successmessage"] = "Staff member added successfully."
                            except Exception:
                                params["success"] = 1
                                params["successmessage"] = "Staff member added successfully. But Email failed to deliver"
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
        admin_count = AdminData.objects.all().order_by('admin_id')
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
                        return redirect('/adminportal/staffprofile/'+adminid)
            
            #upload data logic
            if "uploaddata" in request.POST:
                name = request.POST["fullname"].title()
                contact = request.POST["contact"]
                address = request.POST["address"]
                dob = request.POST.get("dob", "")
                status = request.POST.get("status","Active")
                update = AdminData.objects.filter(admin_id=adminid).update(admin_name=name, admin_contact=contact, admin_address=address, admin_dob=dob, admin_status=status)
                if update == 0:
                    params["dataerror"] = 1
                else:
                    return redirect('/adminportal/staffprofile/'+adminid)
        
        admin = AdminData.objects.filter(admin_id=adminid)
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
                            name = request.POST["name"].title()
                            about = request.POST["about"]
                            contact = request.POST["contact"]
                            address = request.POST["address"]
                            dob = request.POST.get("dob","")
                            status = request.POST.get("status","Active")
                            height = request.POST["height1"]+","+request.POST["height2"]
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

        trainer_count = TrainerData.objects.all().reverse()
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
                        return redirect('/adminportal/trainersprofile/'+trainerid)
            
            #upload data logic
            if "uploaddata" in request.POST:
                name = request.POST["name"].title()
                about = request.POST.get("about","")
                contact = request.POST["contact"]
                address = request.POST["address"]
                dob = request.POST.get("dob","")
                status = request.POST.get("status","Active")
                height = request.POST["height1"]+","+request.POST["height2"]
                weight = request.POST["weight"]
                fb = request.POST["fb"]
                ig = request.POST["ig"]
                update = TrainerData.objects.filter(trainer_id=trainerid).update(trainer_name=name, trainer_contact=contact, trainer_about=about, trainer_height=height, trainer_weight=weight, trainer_fb= fb, trainer_ig= ig, trainer_address=address, trainer_dob=dob, trainer_status=status)
                if update == 0:
                    params["dataerror"] = 1
                else:
                    return redirect('/adminportal/trainersprofile/'+trainerid)

        trainer = TrainerData.objects.filter(trainer_id = trainerid)
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
        params={"error":0, "errormessage":"", "success":0, "successmessage":""}
        class_count = ClassData.objects.all().order_by('class_id')

        # add Class logic
        if "addclass" in request.POST:
            if len(class_count) == 0:
                new_id = "cls1"
            else:
                new_id = "cls" + str((int(class_count[len(class_count)-1].class_id[-1])+1))
            
            try:
                file = request.FILES['picture']
            except MultiValueDictKeyError:
                file = False
        
            if file != False:
                if imghdr.what(file) == None:
                    params["error"] = 1
                    params["errormessage"] = "Select a suitable image file type"
                else:
                    try:
                        name = request.POST["name"].title()
                        desc = request.POST.get("desc","")
                        days = " ".join(request.POST.getlist("days[]",""))
                        stime = request.POST.get("stime","")
                        etime = request.POST.get("etime","")
                        trainer = request.POST.get("trainer","")
                        picture = new_id+".jpg"
                        added_by = request.session["userid"]
                        added_on = datetime.datetime.now().strftime("%Y-%m-%d")
                        picture = new_id+".jpg"
                        new_class = ClassData(class_id=new_id, class_name=name, class_desc=desc, class_img_name=picture, class_days=days, class_stime=stime, class_etime=etime, class_trainer=trainer, class_added_by=added_by, class_added_on=added_on)
                        new_class.save()
                        image_64_encode = base64.encodebytes(file.read())
                        image_64_decode = base64.decodebytes(image_64_encode)
                        image_result = open("media\\adminportal\\class\\"+picture, 'wb')
                        image_result.write(image_64_decode)
                        params["success"] = 1
                        params["successmessage"] = "Class added successfully."
                    except Exception:
                        params["error"] = 1
                        params["errormessage"] = "Something went wrong. Try again later."

        # delete class logic
        if "deleteclass" in request.POST:
            del_id = request.POST["id"]
            class_delete = ClassData.objects.filter(class_id = del_id).delete()
            if class_delete[0] == 1:
                try:
                    os.remove("media\\adminportal\\class\\"+del_id+".jpg")
                    params["success"] = 1
                    params["successmessage"] = "Class successfully deleted."
                except Exception:
                    pass
            else:
                params["error"] = 1
                params["errormessage"] = "Something went wrong. Try again later."
        

        #main page logic
        trainers = TrainerData.objects.all() #for trainers on html5 select
        params["trainers"] = trainers

        classes = {}
        class_count = ClassData.objects.all().order_by('class_id')
        for classSingle in class_count:
            classes[classSingle.class_id] = {
                "id": classSingle.class_id, 
                "name": classSingle.class_name, 
                "desc": classSingle.class_desc, 
                "trainer": trainers.filter(trainer_id=classSingle.class_trainer)[0].trainer_name,
                "days": classSingle.class_days,
                "stime": classSingle.class_stime,
                "etime": classSingle.class_etime,
                "added_by": classSingle.class_added_by,
                "added_on": classSingle.class_added_on,    
            }
            
        params["classes"] = classes
        return render(request, 'adminportal/classes.html', params)
    else:
        return redirect('/adminportal/login/')
    





def classesedit(request, classid):
    if "userid" in request.session and request.session["userrole"] == "Admin" :
        params={"error":0, "errormessage":""}
        
        if "updateclass" in request.POST:
            try:
                file = request.FILES['picture']
            except MultiValueDictKeyError:
                file = False
            if file != False:
                if imghdr.what(file) == None:
                    params["error"] = 1
                    params["errormessage"] = "Select a suitable image file type"
                else:
                    try:
                        image_64_encode = base64.encodebytes(file.read())
                        image_64_decode = base64.decodebytes(image_64_encode)
                        image_result = open("media\\adminportal\\class\\"+classid+".jpg", 'wb')
                        image_result.write(image_64_decode)
                    except Exception:
                        params["error"] = 1
                        params["errormessage"] = "Something went wrong while uploading imaging. Try again later."
            
            
            try:
                name = request.POST["name"].title()
                desc = request.POST.get("desc","")
                days = " ".join(request.POST.getlist("days[]",""))
                if days == "":
                    days = request.POST.get("cdays","")     
                stime = request.POST.get("stime","")
                etime = request.POST.get("etime","")
                trainer = request.POST.get("trainer","")
                update = ClassData.objects.filter(class_id=classid).update(class_name=name, class_desc=desc, class_days=days, class_stime=stime, class_etime=etime, class_trainer=trainer)
                if update == 0:
                    params["error"] = 1
                    params["errormessage"] = "Something went wrong while updating the data. Try again later."
            except Exception:
                params["error"] = 1
                params["errormessage"] = "Something went wrong while updating the data. Try again later."

                    

        #main page logic
        trainers = TrainerData.objects.all() #for trainers on html5 select
        params["trainers"] = trainers

        classSingle = ClassData.objects.filter(class_id=classid)[0]
        params["class"] = {
            "id": classSingle.class_id,
            "name": classSingle.class_name,
            "desc": classSingle.class_desc,
            "days": classSingle.class_days,
            "trid": classSingle.class_trainer,
            "trname": trainers.filter(trainer_id = classSingle.class_trainer)[0].trainer_name,
            "stime": classSingle.class_stime,
            "etime": classSingle.class_etime
        }
        return render(request, 'adminportal/editclass.html', params)
    else:
        return redirect('/adminportal/login/')
    





def expenses(request):
    if "userid" in request.session and request.session["userrole"] == "Admin" :

        params={"error":0, "errormessage":"", "success":0, "successmessage":""}
        expense_count = ExpenseData.objects.all().order_by('expense_id')

        # add expense logic
        if "addexpense" in request.POST:
            if len(expense_count) == 0:
                new_id = "exp1"
            else:
                new_id = "exp" + str((int(expense_count[len(expense_count)-1].expense_id[-1])+1))
            try:
                name = request.POST["name"].title()
                price = request.POST.get("price","")
                month = request.POST.get("month","")
                year = request.POST.get("year","")
                added_by = request.session["userid"]
                added_on = datetime.datetime.now().strftime("%Y-%m-%d")
                new_expense = ExpenseData(expense_id=new_id, expense_name=name, expense_price=price, expense_month=month, expense_year=year, expense_added_by=added_by, expense_added_on=added_on)
                new_expense.save()
                params["success"] = 1
                params["successmessage"] = "Expense entry added successfully."
            except Exception:
                params["error"] = 1
                params["errormessage"] = "Entry '"+name+"' already exists for "+month+" "+year+". Try changing the name."

        # delete expense logic
        if "deleteexpense" in request.POST:
            del_id = request.POST["id"]
            expense_delete = ExpenseData.objects.filter(expense_id = del_id).delete()
            if expense_delete[0] == 1:
                params["success"] = 1
                params["successmessage"] = "Expense entry successfully deleted."
            else:
                params["error"] = 1
                params["errormessage"] = "Something went wrong. Try again later."

        #page logic
        params["expense"] = ExpenseData.objects.all().order_by('expense_id')
        return render(request, 'adminportal/expenses.html', params)
    else:
        return redirect('/adminportal/login/')
    





def expensesedit(request, expid):
    if "userid" in request.session and request.session["userrole"] == "Admin" :
        params={"error":0, "errormessage":""}

        if "updateexpense" in request.POST:
            try:
                name = request.POST["name"].title()
                price = request.POST.get("price","")
                month = request.POST.get("month","")
                year = request.POST.get("year","")
                update = ExpenseData.objects.filter(expense_id=expid).update(expense_name=name, expense_price=price, expense_month=month, expense_year=year)
                if update == 0:
                    params["error"] = 1
                    params["errormessage"] = "Something went wrong while updating the data. Try again later."
            except Exception:
                params["error"] = 1
                params["errormessage"] = "Can't update to '"+name+" for "+month+", "+year+"' because it already exists"

        params["expense"] = ExpenseData.objects.filter(expense_id=expid)[0]
        return render(request, 'adminportal/editexpense.html', params)
    else:
        return redirect('/adminportal/login/')
    





def packages(request):
    if "userid" in request.session and request.session["userrole"] == "Admin" :
        params={"error":0, "errormessage":"", "success":0, "successmessage":""}
        package_count = PackageData.objects.all().order_by('package_id')
        
        #add package logic
        if "addpackage" in request.POST:
            if len(package_count) == 0:
                new_id = "pkg1"
            else:
                new_id = "pkg" + str((int(package_count[len(package_count)-1].package_id[-1])+1))
             
            name = request.POST["name"].upper()

            if package_count.filter(package_name=name).exists():
                params["error"] = 1
                params["errormessage"] = "Package with name '"+name+"' already exists!"
            else:
                try:
                    desc = request.POST["desc"]
                    features = request.POST["features"]
                    price = request.POST["price"]
                    added_by = request.session["userid"]
                    added_on = datetime.datetime.now().strftime("%Y-%m-%d")
                    new_package = PackageData(package_id=new_id, package_name=name, package_desc=desc, package_price=price, package_features=features, package_added_by=added_by, package_added_on=added_on)
                    new_package.save()
                    params["success"] = 1
                    params["successmessage"] = "Package added successfully."
                except Exception:
                    params["error"] = 1
                    params["errormessage"] = "Something went wrong. Try again later."
        
        #delete packages logic
        if "deletepackage" in request.POST:
            del_id = request.POST["id"]
            package_delete = PackageData.objects.filter(package_id = del_id).delete()
            if package_delete[0] == 1:
                params["success"] = 1
                params["successmessage"] = "Package successfully deleted."
            else:
                params["error"] = 1
                params["errormessage"] = "Something went wrong. Try again later."
            
        
        #page logic
        package_count = PackageData.objects.all().order_by('package_id')
        packages = {}
        for package in package_count:
            features = [feature.lstrip().rstrip() for feature in package.package_features.split(",")]
            packages[package.package_id] = {
                "id":package.package_id, 
                "name": package.package_name, 
                "desc": package.package_desc, 
                "features": features, 
                "price": '{:,}'.format(package.package_price)
            }
        params["package_list"] = packages 
        return render(request, 'adminportal/packages.html', params)
    else:
        return redirect('/adminportal/login/')
    





def packagesedit(request, pkgid):
    if "userid" in request.session and request.session["userrole"] == "Admin" :
        params = {"dataerror":0, "message":""}

        #upload data logic
        if "uploaddata" in request.POST:
            name = request.POST["name"].upper()
            desc = request.POST["desc"]
            features = request.POST["features"]
            price = request.POST["price"]
            try:
                update = PackageData.objects.filter(package_id=pkgid).update(package_name=name, package_price=price, package_desc=desc, package_features=features)
                if update == 0:
                    params["dataerror"] = 1
                    params["message"] = "Something went wrong. Try again later."
                else:
                    return redirect('/adminportal/packages/')
            except Exception:
                params["dataerror"] = 1
                params["message"] = "Cant change the name to '"+name+"'. It already exists."

        package = PackageData.objects.filter(package_id=pkgid)
        params["package"] = package[0]
        return render(request, 'adminportal/editpackage.html', params)
    else:
        return redirect('/adminportal/login/')
    





def equipments(request):
    if "userid" in request.session and request.session["userrole"] == "Admin" :
        params={"error":0, "errormessage":"", "success":0, "successmessage":""}
        equipment_count = EquipmentData.objects.all().order_by('equipment_id')
        #add equipment logic
        if "addequipment" in request.POST:
            if len(equipment_count) == 0:
                new_id = "eqp1"
            else:
                new_id = "eqp" + str((int(equipment_count[len(equipment_count)-1].equipment_id[-1])+1))
            
            try:
                name = request.POST["name"].title()
                brand = request.POST["brand"]
                quantity = int(request.POST["quantity"])
                price = int(request.POST["price"])
                total = quantity * price
                added_by = request.session["userid"]
                added_on = datetime.datetime.now().strftime("%Y-%m-%d")
                new_equipment = EquipmentData(equipment_id=new_id, equipment_name=name, equipment_brand=brand, equipment_quantity=quantity, equipment_price=price, equipment_total=total, equipment_added_by=added_by, equipment_added_on=added_on)
                new_equipment.save()
                params["success"] = 1
                params["successmessage"] = "Equipment added successfully."
            except Exception:
                params["error"] = 1
                params["errormessage"] = "Something went wrong. Try again later."
            
        #delete packages logic
        if "deleteequipment" in request.POST:
            del_id = request.POST["id"]
            equipment_delete = EquipmentData.objects.filter(equipment_id = del_id).delete()
            if equipment_delete[0] == 1:
                params["success"] = 1
                params["successmessage"] = "Equipment successfully deleted."
            else:
                params["error"] = 1
                params["errormessage"] = "Something went wrong. Try again later."
        
        #page logic
        equipments = EquipmentData.objects.all().order_by('equipment_id')
        params["equipments"] = equipments
        return render(request, 'adminportal/equipments.html', params)
    else:
        return redirect('/adminportal/login/')
    





def equipmentsedit(request, eqid):
    if "userid" in request.session and request.session["userrole"] == "Admin" :
        params = {"dataerror":0, "message":""}

        if "updateequipment" in request.POST:
            try:
                name = request.POST["name"].title()
                brand = request.POST["brand"]
                quantity = int(request.POST["quantity"])
                price = int(request.POST["price"])
                total = quantity * price
                update = EquipmentData.objects.filter(equipment_id=eqid).update(equipment_name=name, equipment_brand=brand, equipment_quantity=quantity, equipment_price=price, equipment_total=total)
                if update == 0:
                    params["dataerror"] = 1
                    params["message"] = "Something went wrong. Try again later."
                else:
                    return redirect('/adminportal/equipments/')
            except Exception:
                params["dataerror"] = 1
                params["message"] = "Something went wrong while updating. Try again later."


        equipment = EquipmentData.objects.filter(equipment_id=eqid)
        params["equipment"] = equipment[0]
        return render(request, 'adminportal/editequipments.html', params)
    else:
        return redirect('/adminportal/login/')
    





def exercises(request):
    if "userid" in request.session and request.session["userrole"] == "Admin" :
        
        params={"error":0, "errormessage":"", "success":0, "successmessage":""}
        exercise_count = ExerciseData.objects.all().order_by('exercise_id')

        # add exercise logic
        if "addexercise" in request.POST:
            if len(exercise_count) == 0:
                new_id = "exr1"
            else:
                new_id = "exr" + str((int(exercise_count[len(exercise_count)-1].exercise_id[-1])+1))
            
            try:
                file = request.FILES['picture']
            except MultiValueDictKeyError:
                file = False
        
            if file != False:
                if imghdr.what(file) == None:
                    params["error"] = 1
                    params["errormessage"] = "Select a suitable image file type"
                else:
                    try:
                        name = request.POST["name"].title()
                        desc = request.POST.get("desc","")
                        equipment = request.POST.get("equipment","").title()
                        muscle = request.POST.get("muscle","")
                        sets = request.POST.get("sets","")
                        tutorial = request.POST.get("tutorial","")
                        picture = new_id+".jpg"
                        added_by = request.session["userid"]
                        added_on = datetime.datetime.now().strftime("%Y-%m-%d")
                        new_exercise = ExerciseData(exercise_id=new_id, exercise_name=name, exercise_desc=desc, exercise_img_name=picture, exercise_equipment=equipment, exercise_muscle=muscle, exercise_tutorial=tutorial, exercise_sets=sets, exercise_added_by=added_by, exercise_added_on=added_on)
                        new_exercise.save()
                        image_64_encode = base64.encodebytes(file.read())
                        image_64_decode = base64.decodebytes(image_64_encode)
                        image_result = open("media\\adminportal\\exercise\\"+picture, 'wb')
                        image_result.write(image_64_decode)
                        params["success"] = 1
                        params["successmessage"] = "Exercise added successfully."
                    except Exception:
                        params["error"] = 1
                        params["errormessage"] = "Something went wrong. Try again later."

        # delete trainer logic
        if "deleteexercise" in request.POST:
            del_id = request.POST["id"]
            exercise_delete = ExerciseData.objects.filter(exercise_id = del_id).delete()
            if exercise_delete[0] == 1:
                try:
                    os.remove("media\\adminportal\\exercise\\"+del_id+".jpg")
                    params["success"] = 1
                    params["successmessage"] = "Class successfully deleted."
                except Exception:
                    pass
            else:
                params["error"] = 1
                params["errormessage"] = "Something went wrong. Try again later."

        params["exercises"] =  ExerciseData.objects.all().order_by('exercise_id')
        return render(request, 'adminportal/exercise.html', params)
    else:
        return redirect('/adminportal/login/')
    





def exercisesedit(request, exrid):
    params={"error":0, "errormessage":""}
    if "userid" in request.session and request.session["userrole"] == "Admin" :
        if "updateexercise" in request.POST:
            try:
                file = request.FILES['picture']
            except MultiValueDictKeyError:
                file = False
            if file != False:
                if imghdr.what(file) == None:
                    params["error"] = 1
                    params["errormessage"] = "Select a suitable image file type"
                else:
                    try:
                        image_64_encode = base64.encodebytes(file.read())
                        image_64_decode = base64.decodebytes(image_64_encode)
                        image_result = open("media\\adminportal\\exercise\\"+exrid+".jpg", 'wb')
                        image_result.write(image_64_decode)
                    except Exception:
                        params["error"] = 1
                        params["errormessage"] = "Something went wrong while uploading imaging. Try again later."
            
            
            try:
                name = request.POST["name"].title()
                desc = request.POST.get("desc","")
                equipment = request.POST.get("equipment","").title()
                muscle = request.POST.get("muscle","")
                sets = request.POST.get("sets","")
                tutorial = request.POST.get("tutorial","")
                update = ExerciseData.objects.filter(exercise_id=exrid).update(exercise_name=name, exercise_desc=desc, exercise_equipment=equipment, exercise_muscle=muscle, exercise_tutorial=tutorial, exercise_sets=sets)
                if update == 0:
                    params["error"] = 1
                    params["errormessage"] = "Something went wrong while updating the data. Try again later."
            except Exception:
                params["error"] = 1
                params["errormessage"] = "Something went wrong while updating the data. Try again later."

        
        params["exercise"] = ExerciseData.objects.filter(exercise_id = exrid)[0]
        return render(request, 'adminportal/editexercise.html', params)
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

        params={"error":0, "errormessage":"", "success":0, "successmessage":""}
        diet_count = DietData.objects.all().order_by('diet_id')

        # add diet logic
        if "adddiet" in request.POST:
            if len(diet_count) == 0:
                new_id = "dt1"
            else:
                new_id = "dt" + str((int(diet_count[len(diet_count)-1].diet_id[-1])+1))
            try:
                name = request.POST["name"].title()
                desc = request.POST.get("desc","")
                json = request.POST.get("dietjson","")
                added_by = request.session["userid"]
                added_on = datetime.datetime.now().strftime("%Y-%m-%d")
                new_diet = DietData(diet_id=new_id, diet_name=name, diet_desc=desc, diet_json=json, diet_added_by=added_by, diet_added_on=added_on)
                new_diet.save()
                params["success"] = 1
                params["successmessage"] = "Diet added successfully."
            except Exception:
                params["error"] = 1
                params["errormessage"] = "Something went wrong. Try again later."

        # delete expense logic
        if "deletediet" in request.POST:
            del_id = request.POST["id"]
            diet_delete = DietData.objects.filter(diet_id = del_id).delete()
            if diet_delete[0] == 1:
                params["success"] = 1
                params["successmessage"] = "Diet successfully deleted."
            else:
                params["error"] = 1
                params["errormessage"] = "Something went wrong. Try again later."

        #page logic
        params["diets"] = DietData.objects.all().order_by('diet_id')
        return render(request, 'adminportal/diet.html', params)
    else:
        return redirect('/adminportal/login/')
    





def dietview(request, dtid):
    if "userid" in request.session and request.session["userrole"] == "Admin" :
        params={}
        diet = DietData.objects.filter(diet_id=dtid)[0]
        params["name"] = diet.diet_name
        params["desc"] = diet.diet_desc
        params["plan"] = json.loads(diet.diet_json)
        return render(request, 'adminportal/dietview.html', params)
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
    



