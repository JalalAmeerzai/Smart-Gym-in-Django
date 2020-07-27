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
            return JsonResponse({"state": state})
        else:
            return JsonResponse({"message": "can't locate user"})



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
            image = open('media\\adminportal\\member\\'+member[0].member_img_name, 'rb')
            image_read = image.read()
            response["image"] = base64.b64encode(image_read).decode('utf-8')
            try:
                response["routine"] = json.loads(RoutineData.objects.filter(routine_id = member[0].member_routine)[0].routine_json)[user_request["day"].lower()]
                for key, routine in response["routine"].items():
                    imagestr = base64.b64encode(open('media\\adminportal\\exercise\\'+routine["exercise"]+".jpg", 'rb').read()).decode('utf-8')
                    response["routine"][key]["name"] = ExerciseData.objects.filter(exercise_id = routine["exercise"])[0].exercise_name
                    response["routine"][key]["image"] = imagestr
            except Exception:
                response["routine"] = 0
            try:
                response["diet"] = json.loads(DietData.objects.filter(diet_id = member[0].member_diet)[0].diet_json)[user_request["day"].lower()]
            except Exception:
                response["diet"] = 0
            return JsonResponse(response)
        else:
            return JsonResponse({"message": "can't locate user"})



@csrf_exempt
def createsuperuser(request):
    adm = AdminData(admin_id="adm1", admin_name="Super User", admin_email="super@user.com", admin_password="superuser123", admin_contact="03031234567", admin_address="Super Street Block Super, supercity", admin_dob="1994-10-02", admin_status="Active", admin_role="Admin", admin_img_name="adm1.jpg", admin_added_by="superuser", admin_added_on="2020-07-28")
    adm.save()
    return HttpResponse("success")



@csrf_exempt
def userdiet(request):
    if request.method == "POST":
        user_request = json.loads(request.body)
        try:
            diet = json.loads(DietData.objects.filter(diet_id=MemberData.objects.filter(member_id=user_request["id"])[0].member_diet)[0].diet_json)
            return JsonResponse(diet)
        except Exception:
            diet = 0
            return JsonResponse({"diet": diet})



@csrf_exempt
def userroutine(request):
    if request.method == "POST":
        user_request = json.loads(request.body)
        try:
            routine = json.loads(RoutineData.objects.filter(routine_id=MemberData.objects.filter(member_id=user_request["id"])[0].member_routine)[0].routine_json)
            for day in routine:
                for exercise in routine[day]:
                    try:
                        routine[day][exercise]["name"] = ExerciseData.objects.filter(exercise_id=routine[day][exercise]["exercise"])[0].exercise_name
                        imagestr = base64.b64encode(open('media\\adminportal\\exercise\\'+routine[day][exercise]["exercise"]+".jpg", 'rb').read()).decode('utf-8')
                        routine[day][exercise]["image"] = imagestr
                    except Exception:
                        routine[day][exercise]["name"] = " - "
                        routine[day][exercise]["image"] = 0
            return JsonResponse(routine)
        except Exception:
            routine = 0
            return JsonResponse({"routine": routine})


@csrf_exempt
def identifymachine(request):
    if request.method == "POST":
        user_request = json.loads(request.body)
        image_base64_string = user_request["image"]
        image_64_decode = base64.decodebytes(image_base64_string.encode('ascii'))
        image_result = open("media\\adminportal\\identify\\machine.jpg", 'wb')
        image_result.write(image_64_decode)
        machine_name = "bench" #machine learning identification to return output string machine name here
        try:
            exercises = ExerciseData.objects.filter(exercise_equipment__icontains=machine_name)
            exercises_to_send = {}
            i = 1
            for exercise in exercises:
                exercises_to_send["Exercise"+str(i)] = {"name": exercise.exercise_name, "equipment": exercise.exercise_equipment, "video": exercise.exercise_tutorial}
                i = i+1
        except Exception:
            pass    
        
        if exercises_to_send == {}:
            exercises_to_send["message"] = "no exercises found"
        
        return JsonResponse(exercises_to_send)


@csrf_exempt
def listofroutines(request):
    if request.method == "POST":
        routines = RoutineData.objects.all()
        routines_to_send = {}
        if len(routines) > 0:
            i = 1
            for routine in routines:
                imagestr = base64.b64encode(open('media\\adminportal\\routine\\'+routine.routine_id+".jpg", 'rb').read()).decode('utf-8')
                routines_to_send["Routine"+str(i)] = {"id": routine.routine_id, "name": routine.routine_name, "description": routine.routine_desc, "image": imagestr}
                i = i + 1
            return JsonResponse(routines_to_send)
        else:
            return JsonResponse({"message": "no routines found"})



@csrf_exempt
def viewroutine(request):
    if request.method == "POST":
        user_request = json.loads(request.body)




#@csrf_exempt
#def productapi(request):
    #if request.method=="GET":
        #jalal = [{'id':'existing','name':'test user'}]
        #jalal.append({'id': request.GET.get('id', ''), 'name': request.GET.get('name', '')})
        #products = Product.objects.all()
        #return HttpResponse(json.dumps(jalal,  default=str))
        
        #objectreturn = {}
        #for i in range(1,4):
            #obj = "obj"+str(i)
            #objectreturn[obj] = {"id": i, "name": "test"+str(i)}
        #objectreturn["obj"+str(request.GET.get('id', ''))] = {'id': request.GET.get('id', ''), 'name': request.GET.get('name', '')}
        #return JsonResponse(objectreturn)
        
        #getting raw data in the form of json and converting it into json
        #dicts = json.loads(request.body) # to get the raw json data from request and convert it into a json or a dictionary   
        #return JsonResponse(dicts)

        #return HttpResponse(len(request.body))





            #image = open('media\\adminportal\\member\\'+member[0].member_img_name, 'rb')
            #image_read = image.read()
            #string = base64.b64encode(image_read)
            
            #image_64_encode = base64.encodebytes(image_read)
            #image_64_decode = base64.decodebytes(imgstr.encode('ascii'))
            #print(type(image_64_encode),"\n\n", image_64_encode )
            #image_result = open('cv233.png', 'wb') # create a writable image and write the decoding result
            #image_result.write(image_64_decode)




            #slikeroperator
            #ExerciseData.objects.filter(exercise_equipment__icontains='bench')[0].exercise_name