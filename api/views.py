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
from django.views.decorators.csrf import csrf_exempt






@csrf_exempt
def login(request):
    if request.method == "POST":
        #return JsonResponse(json.loads(RoutineData.objects.filter(routine_id="rtn1")[0].routine_json))
        response = {}
        user_request = json.loads(request.body)
        user = MemberData.objects.filter(member_email=user_request["email"].lower(), member_password=user_request["password"])
        if len(user) > 0:
            status = user[0].member_status
            if status == "Active":
                userid = user[0].member_id
                state = 1
                height = user[0].member_height
                weight = user[0].member_weight
                if weight == "" or height =="":
                    message = "register"
                else:
                    message = "login"
                response = {"id": userid, "state": state, "message": message}
                return JsonResponse(response)
            else:
                state = - 1
                message = "Account has been disabled by an admin"
                response = {"state": state, "message": message}
                return JsonResponse(response)
        else:
            state = 0
            message = "Wrong Username/Password"
            response = {"state": state, "message": message}
            return JsonResponse(response)



@csrf_exempt
def putmeasurements(request):
    if request.method == "POST":
        user_request = json.loads(request.body)
        member = MemberData.objects.filter(member_id = user_request["id"])
        if len(member) > 0:
            update = MemberData.objects.filter(member_id = user_request["id"]).update(member_weight=user_request["weight"], member_height=user_request["height"])
            if update == 1:
                state = 1
            else:
                state = 0
            return HttpResponse(state)
        else:
            return HttpResponse("can't locate user")



@csrf_exempt
def homescreen(request):
    if request.method == "POST":
        user_request = json.loads(request.body)
        member = MemberData.objects.filter(member_id = user_request["id"])
        if len(member) > 0:
            response = {}
            response["id"] = member[0].member_id
            response["name"] = member[0].member_name
            response["contact"] = member[0].member_contact
            response["email"] = member[0].member_email
            response["address"] = member[0].member_address
            response["dob"] = member[0].member_dob
            response["height"] = member[0].member_height
            response["weight"] = member[0].member_weight
            image = open('./media/adminportal/member/'+member[0].member_img_name, 'rb')
            image_read = image.read()
            response["image"] = base64.b64encode(image_read).decode('utf-8')
            try:
                response["routine"] = json.loads(RoutineData.objects.filter(routine_id = member[0].member_routine)[0].routine_json)[user_request["day"].lower()]
                for key, routine in response["routine"].items():
                    imagestr = base64.b64encode(open('./media/adminportal/exercise/'+routine["exercise"]+".jpg", 'rb').read()).decode('utf-8')
                    response["routine"][key]["name"] = ExerciseData.objects.filter(exercise_id = routine["exercise"])[0].exercise_name
                    response["routine"][key]["image"] = imagestr
                
                routine_list = []
                for routine in response["routine"].values():
                    routine_list.append(routine)
                
                response["routine"] = routine_list
            except Exception:
                response["routine"] = []
            try:
                response["diet"] = json.loads(DietData.objects.filter(diet_id = member[0].member_diet)[0].diet_json)[user_request["day"].lower()]
                diet_list = []
                for diet in response["diet"].values():
                    diet_list.append(diet)
                response["diet"] = diet_list
            except Exception:
                response["diet"] = []
            return JsonResponse(response)
        else:
            return HttpResponse("can't locate user")



@csrf_exempt
def createsuperuser(request):
    adm = AdminData(admin_id="adm1", admin_name="Super User", admin_email="super@user.com", admin_password="superuser123", admin_contact="03031234567", admin_address="Super Street Block Super, supercity", admin_dob="1994-10-02", admin_status="Active", admin_role="Admin", admin_img_name="adm1.jpg", admin_added_by="superuser", admin_added_on="2020-07-28")
    adm.save()
    return HttpResponse("success")



@csrf_exempt
def userdiet(request):
    if request.method == "POST":
        user_request = json.loads(request.body)
        plan = {"monday": [], "tuesday": [], "wednesday":[], "thursday": [], "friday": [], "saturday":[], "sunday": []}
        try:
            diet = json.loads(DietData.objects.filter(diet_id=MemberData.objects.filter(member_id=user_request["id"])[0].member_diet)[0].diet_json)
            for d_monday in diet["monday"].values():
                plan["monday"].append(d_monday) 

            for d_tuesday in diet["tuesday"].values():
                plan["tuesday"].append(d_tuesday) 

            for d_wednesday in diet["wednesday"].values():
                plan["wednesday"].append(d_wednesday)
                
            for d_thursday in diet["thursday"].values():
                plan["thursday"].append(d_thursday)

            for d_friday in diet["friday"].values():
                plan["friday"].append(d_friday)     
            
            for d_saturday in diet["saturday"].values():
                plan["saturday"].append(d_saturday)  
            
            for d_sunday in diet["sunday"].values():
                plan["sunday"].append(d_sunday)  

        except Exception:
            plan = {"monday": [], "tuesday": [], "wednesday":[], "thursday": [], "friday": [], "saturday":[], "sunday": []}
            
        return JsonResponse(plan)



@csrf_exempt
def userroutine(request):
    if request.method == "POST":
        plan = {"monday": [], "tuesday": [], "wednesday":[], "thursday": [], "friday": [], "saturday":[], "sunday": []}
        user_request = json.loads(request.body)
        try:
            routine = json.loads(RoutineData.objects.filter(routine_id=MemberData.objects.filter(member_id=user_request["id"])[0].member_routine)[0].routine_json)
            for day in routine:
                for exercise in routine[day]:
                    try:
                        routine[day][exercise]["name"] = ExerciseData.objects.filter(exercise_id=routine[day][exercise]["exercise"])[0].exercise_name
                        imagestr = base64.b64encode(open('./media/adminportal/exercise/'+routine[day][exercise]["exercise"]+".jpg", 'rb').read()).decode('utf-8')
                        routine[day][exercise]["image"] = imagestr
                    except Exception:
                        routine[day][exercise]["name"] = " - "
                        routine[day][exercise]["image"] = 0
            

            for d_monday in routine["monday"].values():
                plan["monday"].append(d_monday) 

            for d_tuesday in routine["tuesday"].values():
                plan["tuesday"].append(d_tuesday) 

            for d_wednesday in routine["wednesday"].values():
                plan["wednesday"].append(d_wednesday)
                
            for d_thursday in routine["thursday"].values():
                plan["thursday"].append(d_thursday)

            for d_friday in routine["friday"].values():
                plan["friday"].append(d_friday)     
            
            for d_saturday in routine["saturday"].values():
                plan["saturday"].append(d_saturday)  
            
            for d_sunday in routine["sunday"].values():
                plan["sunday"].append(d_sunday)


        except Exception:
            plan = {"monday": [], "tuesday": [], "wednesday":[], "thursday": [], "friday": [], "saturday":[], "sunday": []}
        
        return JsonResponse(plan)



@csrf_exempt
def identifymachine(request):
    if request.method == "POST":
        exercise_list = []
        user_request = json.loads(request.body)
        image_base64_string = user_request["image"]
        image_64_decode = base64.decodebytes(image_base64_string.encode('ascii'))
        image_result = open("./media/adminportal/identify/machine.jpg", 'wb')
        image_result.write(image_64_decode)
        machine_name = "bench" #machine learning identification to return output string machine name here
        try:
            exercises = ExerciseData.objects.filter(exercise_equipment__icontains=machine_name)
            for exercise in exercises:
                exercise_list.append({"name": exercise.exercise_name, "equipment": exercise.exercise_equipment, "video": exercise.exercise_tutorial})
        except Exception:
            pass       
        return JsonResponse({"exercises":exercise_list})



@csrf_exempt
def listofroutines(request):
    if request.method == "GET":
        routines = RoutineData.objects.all()
        routines_list = []
        if len(routines) > 0:
            i = 1
            for routine in routines:
                imagestr = base64.b64encode(open('./media/adminportal/routine/'+routine.routine_id+".jpg", 'rb').read()).decode('utf-8')
                routines_list.append({"id": routine.routine_id, "name": routine.routine_name, "description": routine.routine_desc, "image": imagestr}) 
            return JsonResponse({"routines": routines_list})
        else:
            return JsonResponse({"routines": []})



@csrf_exempt
def viewroutine(request):
    if request.method == "POST":
        user_request = json.loads(request.body)
        try:
            routine = RoutineData.objects.filter(routine_id=user_request["routine"])[0]
            routine_json = json.loads(routine.routine_json)
            for day in routine_json:
                for exercise in routine_json[day]:
                    try:
                        routine_json[day][exercise]["name"] = ExerciseData.objects.filter(exercise_id=routine_json[day][exercise]["exercise"])[0].exercise_name
                        imagestr = base64.b64encode(open('./media/adminportal/exercise/'+routine_json[day][exercise]["exercise"]+".jpg", 'rb').read()).decode('utf-8')
                        routine_json[day][exercise]["image"] = imagestr
                    except Exception:
                        routine_json[day][exercise]["name"] = " - "
                        routine_json[day][exercise]["image"] = 0
            view_routine = {"id": routine.routine_id, "name": routine.routine_name, "description": routine.routine_desc, "image": base64.b64encode(open('./media/adminportal/routine/'+routine.routine_id+".jpg", 'rb').read()).decode('utf-8'), "routine": routine_json}
            return JsonResponse(view_routine)
        except Exception:
            return JsonResponse({})



@csrf_exempt
def followroutine(request):
    if request.method == "POST":
        user_request = json.loads(request.body)
        try:
            update = MemberData.objects.filter(member_id = user_request["id"]).update(member_routine=user_request["routine"])
            if update == 1:
                return HttpResponse(1)
            else:
                return HttpResponse(0)
        except Exception:
            return HttpResponse(0)



@csrf_exempt
def settings(request):
    if request.method == "POST":
        user_request = json.loads(request.body)
        
        if user_request["update"].lower() == "image":
            if len(MemberData.objects.filter(member_id=user_request["id"])) > 0:
                try:
                    imagestr = user_request["image"]
                    image_64_decode = base64.decodebytes(imagestr.encode('ascii'))
                    image_result = open('./media/adminportal/member/'+user_request["id"]+".jpg", 'wb')
                    image_result.write(image_64_decode)
                    return HttpResponse(1)
                except Exception:
                    return HttpResponse(0)
            else:
                return HttpResponse(0)

            
        

        if user_request["update"].lower() == "password":
            if len(MemberData.objects.filter(member_id=user_request["id"], member_password=user_request["oldpassword"])) > 0:
                if len(user_request["newpassword"]) >= 6:
                    update = MemberData.objects.filter(member_id = user_request["id"]).update(member_password=user_request["newpassword"])
                    if update == 1:
                        return HttpResponse(1)
                    else:
                        return HttpResponse(0)
                else:
                    return HttpResponse(0)
            else:
                return HttpResponse("type old password correctly")
        



        if user_request["update"].lower() == "data":
            if len(MemberData.objects.filter(member_id=user_request["id"])) > 0:
                name = user_request["name"].title()
                contact = user_request["contact"]
                dob = user_request["dob"]
                address = user_request["address"]
                height = user_request["height"]
                weight = user_request["weight"]
                update = MemberData.objects.filter(member_id=user_request["id"]).update(member_name=name, member_contact=contact, member_address=address, member_height=height, member_weight=weight, member_dob=dob)
                if update == 1:
                    return HttpResponse(1)
                else:
                    return HttpResponse(0)
            else:
                return HttpResponse("cant locate user")
