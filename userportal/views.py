from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from adminportal.models import AdminData, TrainerData, PackageData, EquipmentData, ClassData, ExpenseData, ExerciseData, DietData, RoutineData, MemberData, MessageData, ArchivedMessageData, ReplyMessageData, AttendanceData, FinanceData, FinanceHistoryData, AdmissionData
from django.utils.datastructures import MultiValueDictKeyError #for files
import base64
import imghdr
import datetime
from datetime import datetime as dt
import os
import re #regex
from django.core.mail import send_mail
import json 
from django.db.models import Avg, Count, Min, Sum




def login(request):
    params = {"error": 0, "errormessage": ""} 
    if "userid" in request.session and request.session["userrole"] == "Member" :
        return redirect('/userportal/user/')
    else:
        if request.method == 'POST': 
            email = request.POST['email'].lower()
            password = request.POST['password']
            member = MemberData.objects.filter(member_password=password, member_email=email)
            if len(member) > 0:
                if member[0].member_status == "Active":
                    request.session["userid"] = member[0].member_id #value to be retrieved from db
                    request.session["userrole"] = "Member" #value to be retrived from db
                    request.session["username"] = member[0].member_name #value to be retrived from db
                    return redirect('/userportal/user/')
                else:
                    params["error"] = 1
                    params["errormessage"] ="Your account is deactivated. Contact gym admin."
            else:
                params["error"] = 1
                params["errormessage"] ="Incorrect Email/Password"
        return render(request, 'userportal/login.html', params)



def passwordlost(request):
    params = {"error":0, "errormessage":"", "success":0, "successmessage": ""}
    if request.method == "POST":
        email = request.POST.get("email","").lower()
        member = MemberData.objects.filter(member_email=email)
        if len(member) > 0:
            password = member[0].member_password
            try:
                send_mail(
                    'Password Lost Request - This Email Contains your Account Credentials',
                    '\nHello '+member[0].member_name+',\nYour account credenatials for smartgym are: \nAccount: '+email+'\nPassword: '+password+"\n\n\nStay Fit.",
                    'SmartGym',
                    [email], 
                )
                params["success"] =1
                params["successmessage"] = "Your credentials have been sent to your email address. Please check."
            except Exception:
                params["error"] = 1
                params["errormessage"] = "Something went wrong. Please try again later."
        else:
            params["error"] = 1
            params["errormessage"] = "'"+email+"' doesnt exist. please type in a correct email address."
    return render(request, 'userportal/lost-password.html', params)



def logout(request):
    if "userid" in request.session and "userrole" in request.session:
        del request.session["userid"]
        del request.session["userrole"]
        del request.session["username"]
    return redirect('/userportal/login/')




def userprofile(request):
    if "userid" in request.session and request.session["userrole"] == "Member" :
        memid = request.session["userid"]
        params={"nodietexist":0, "noroutineexist":0}
        
        try:
            params["member"] = MemberData.objects.filter(member_id=memid)[0]
        except Exception:
            return redirect("/adminportal/members/")
        
        days = ("monday","tuesday","wednesday","thursday","friday","saturday","sunday")
        
        if params["member"].member_diet == "":
            params["nodietexist"] = 1
        else:
            diet = json.loads(DietData.objects.filter(diet_id = params["member"].member_diet)[0].diet_json)
            params["diet"] = diet[days[datetime.datetime.now().weekday()]]
            

        if params["member"].member_routine == "":
            params["noroutineexist"] = 1
        else:
            try:
                routine = json.loads(RoutineData.objects.filter(routine_id = params["member"].member_routine)[0].routine_json)
                params["routine"] = routine[days[datetime.datetime.now().weekday()]]
            except Exception:
                pass

            for exercise in params["routine"]:
                try:
                    params["routine"][exercise]["exname"] = ExerciseData.objects.filter(exercise_id = params["routine"][exercise]["exercise"])[0].exercise_name
                except Exception:
                    params["routine"][exercise]["exname"] = " - "


        #for package
        package = PackageData.objects.filter(package_id = params["member"].member_package)[0]
        package_dict = {
            "name": package.package_name,
            "admission": '{:,}'.format(package.package_admission),
            "price": '{:,}'.format(package.package_price)
        }        
        params["package"] = package_dict
        due_payment = FinanceData.objects.filter(finance_member_id=memid)[0]
        params["payment"] = {
            "due": '{:,}'.format(due_payment.finance_due),
            "balance": '{:,}'.format(due_payment.finance_balance)
        } 


        return render(request, 'userportal/user.html', params)
    else:
        return redirect('/userportal/login/')
        



def settings(request):
    params = {"imageerror":0, "dataerror":0, "passerror1":0, "passerror2":0}
    if "userid" in request.session and request.session["userrole"] == "Member" :

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
                        image_result = open("./media/adminportal/member/"+request.session["userid"]+".jpg", 'wb')
                        image_result.write(image_64_decode)
                        return redirect('/userportal/user/')



            #upload data logic
            if "uploaddata" in request.POST:
                name = request.POST["name"].title()
                contact = request.POST["contact"]
                address = request.POST["address"]
                dob = request.POST.get("dob","")
                
                if request.POST["height1"] == "":
                    height = ""
                else:
                    height = request.POST["height1"]+","+request.POST["height2"]
                weight = request.POST["weight"]
                update = MemberData.objects.filter(member_id=request.session["userid"]).update(member_name=name, member_contact=contact, member_address=address, member_height=height, member_weight=weight, member_dob=dob)
                if update == 0:
                    params["dataerror"] = 1
                else:
                    update_attendance_name = AttendanceData.objects.filter(attendance_member_id=request.session["userid"]).update(attendance_member_name=name)
                    update_finance_name = FinanceData.objects.filter(finance_member_id=request.session["userid"]).update(finance_member_name=name)
                    update_finance_history_name = FinanceHistoryData.objects.filter(fh_member_id=request.session["userid"]).update(fh_member_name=name)



            #upload password logic
            if "uploadpassword" in request.POST:
                password = request.POST["pass"]
                newpassword = request.POST["newpass"]
                passwordtest = MemberData.objects.filter(member_id=request.session["userid"], member_password=password)
                if len(passwordtest) > 0:
                    updatepassword = MemberData.objects.filter(member_id=request.session["userid"]).update(member_password=newpassword)
                    if updatepassword == 0:
                        params["passerror2"] = -1 # unsuccessful
                    else:
                        params["passerror2"] = 1 # successful
                else:
                    params["passerror1"] = 1


        # page logic
        member = MemberData.objects.filter(member_id = request.session["userid"])[0]
        params["member"] = member
        height = member.member_height
        if height == "":
            params["height"] = {"h1": "", "h2":""}
        else:
            h1 = height.split(",")[0]
            h2 = height.split(",")[1]
            params["height"] = {"h1": int(h1), "h2": int(h2)}


        return render(request, 'userportal/settings.html', params)
    else:
        return redirect('/userportal/login/')
    



def routines(request):
    if "userid" in request.session and request.session["userrole"] == "Member" :
        params = {}
        params["routines"] = RoutineData.objects.all()
        params["following"] = MemberData.objects.filter(member_id = request.session["userid"])[0].member_routine
        return render(request, 'userportal/routine.html', params)
    else:
        return redirect('/userportal/login/')
    



def yourroutine(request):
    if "userid" in request.session and request.session["userrole"] == "Member" :

        params={}
        try:
            routine = RoutineData.objects.filter(routine_id=MemberData.objects.filter(member_id=request.session["userid"])[0].member_routine)[0]
            params["name"] = routine.routine_name
            params["desc"] = routine.routine_desc
            params["plan"] = json.loads(routine.routine_json)
            exercise_count = ExerciseData.objects.all().order_by('exercise_id')
            for day in params["plan"]:
                for exercise in params["plan"][day]:
                    try:
                        params["plan"][day][exercise]["exname"] = exercise_count.filter(exercise_id=params["plan"][day][exercise]["exercise"])[0].exercise_name
                    except Exception:
                        params["plan"][day][exercise]["exname"] = " - "
        except Exception:
            pass

        return render(request, 'userportal/yourroutine.html', params)
    else:
        return redirect('/userportal/login/')


def followroutine(request, rtid):
    if "userid" in request.session and request.session["userrole"] == "Member" :
        
        try:
            check_routine = RoutineData.objects.filter(routine_id=rtid)[0]
            update = MemberData.objects.filter(member_id=request.session["userid"]).update(member_routine=rtid)
            return redirect('/userportal/viewroutine/'+rtid)
        except Exception:
            return redirect('/userportal/routines') 

        
        return render(request, 'userportal/createroutine.html')
    else:
        return redirect('/userportal/login/')
    




def viewroutine(request, rtid):
    if "userid" in request.session and request.session["userrole"] == "Member" :
        params={}
        try:
            routine = RoutineData.objects.filter(routine_id=rtid)[0]
        except Exception:
            return redirect("/userportal/routines/")
        
        params["name"] = routine.routine_name
        params["desc"] = routine.routine_desc
        params["plan"] = json.loads(routine.routine_json)
        exercise_count = ExerciseData.objects.all().order_by('exercise_id')
        for day in params["plan"]:
            for exercise in params["plan"][day]:
                try:
                    params["plan"][day][exercise]["exname"] = exercise_count.filter(exercise_id=params["plan"][day][exercise]["exercise"])[0].exercise_name
                except Exception:
                    params["plan"][day][exercise]["exname"] = " - "

        return render(request, 'userportal/routineview.html', params)
    else:
        return redirect('/userportal/login/')
    



def diet(request):
    if "userid" in request.session and request.session["userrole"] == "Member" :
        params={}
        try:
            diet = DietData.objects.filter(diet_id=MemberData.objects.filter(member_id=request.session["userid"])[0].member_diet)[0]
            params["name"] = diet.diet_name
            params["desc"] = diet.diet_desc
            params["plan"] = json.loads(diet.diet_json)
        except Exception:
            pass
        
        return render(request, 'userportal/diet.html', params)
    else:
        return redirect('/userportal/login/')
    



def exercises(request):
    if "userid" in request.session and request.session["userrole"] == "Member" :
        params = {}
        params["exercises"] = ExerciseData.objects.all()
        return render(request, 'userportal/exercise.html', params)
    else:
        return redirect('/userportal/login/')
    
    



def finances(request):
    if "userid" in request.session and request.session["userrole"] == "Member" :
        params = {}
        params["member"] = MemberData.objects.filter(member_id = request.session["userid"])[0]

        package = PackageData.objects.filter(package_id = params["member"].member_package)[0]
        package_dict = {
            "name": package.package_name,
            "admission": '{:,}'.format(package.package_admission),
            "price": '{:,}'.format(package.package_price)
        }        
        params["package"] = package_dict
        due_payment = FinanceData.objects.filter(finance_member_id=request.session["userid"])[0]
        params["payment"] = {
            "due": '{:,}'.format(due_payment.finance_due),
            "balance": '{:,}'.format(due_payment.finance_balance)
        }
        params["transactions"] = FinanceHistoryData.objects.filter(fh_member_id=request.session["userid"]) 
        return render(request, 'userportal/finances.html', params)
    else:
        return redirect('/userportal/login/')
   



def help(request):
    if "userid" in request.session and request.session["userrole"] == "Member" :
        params = {"error":0, "errormessage":"", "success":0, "successmessage": ""}


        if "send" in request.POST:
            
            member = MemberData.objects.filter(member_id=request.session["userid"])[0]
            name = member.member_name.title()
            email = member.member_email.lower()
            subject = request.POST.get("subject","")
            message = request.POST.get("message","")
            time = dt.now().time().strftime("%H:%M")
            date = datetime.datetime.now().strftime("%Y-%m-%d")
            try:
                send_message = MessageData(msg_sender_name=name, msg_sender_email=email, msg_sender_subject=subject, msg_sender_mail=message, msg_sender_date=date, msg_sender_time=time)
                send_message.save()
                params["success"] = 1
                params["successmessage"] = "We have recieved your query. Someone from our team will get back to you soon"
            except Exception:
                params["error"] = 1
                params["errormessage"] = "Something went Wrong. PLease try again later."

        return render(request, 'userportal/help.html', params)
    else:
        return redirect('/userportal/login/')
    



def subscription(request):
    if "userid" in request.session and request.session["userrole"] == "Member" :
         return render(request, 'userportal/subscription.html')
    else:
        return redirect('/userportal/login/')
    
