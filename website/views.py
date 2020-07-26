from django.shortcuts import render
from django.http import HttpResponse
from adminportal.models import ClassData, TrainerData, PackageData, AdmissionData
import datetime

def index(request):
    return render(request, 'website/index.html')



def classes(request):
    params = {}
    classes = ClassData.objects.all().order_by("class_stime")
    classes_single ={}
    timetable = {"monday": {}, "tuesday":{}, "wednesday":{}, "thursday":{}, "friday":{}, "saturday":{}, "sunday":{}}
    for cl in classes:
        try:
            classes_single[cl.class_id] = {"name": cl.class_name, "desc": cl.class_desc, "img": cl.class_img_name, "trainer": TrainerData.objects.filter(trainer_id=cl.class_trainer)[0].trainer_name}
            days = cl.class_days.split(" ")
            if "Monday" in days:
                timetable["monday"][cl.class_id] = {"name": cl.class_name, "trainer": TrainerData.objects.filter(trainer_id=cl.class_trainer)[0].trainer_name, "stime": cl.class_stime, "etime": cl.class_etime}
            if "Tuesday" in days:
                timetable["tuesday"][cl.class_id] = {"name": cl.class_name, "trainer": TrainerData.objects.filter(trainer_id=cl.class_trainer)[0].trainer_name, "stime": cl.class_stime, "etime": cl.class_etime}
            if "Wednesday" in days:
                timetable["wednesday"][cl.class_id] = {"name": cl.class_name, "trainer": TrainerData.objects.filter(trainer_id=cl.class_trainer)[0].trainer_name, "stime": cl.class_stime, "etime": cl.class_etime}
            if "Thursday" in days:
                timetable["thursday"][cl.class_id] = {"name": cl.class_name, "trainer": TrainerData.objects.filter(trainer_id=cl.class_trainer)[0].trainer_name, "stime": cl.class_stime, "etime": cl.class_etime}
            if "Friday" in days:
                timetable["friday"][cl.class_id] = {"name": cl.class_name, "trainer": TrainerData.objects.filter(trainer_id=cl.class_trainer)[0].trainer_name, "stime": cl.class_stime, "etime": cl.class_etime}
            if "Saturday" in days:
                timetable["saturday"][cl.class_id] = {"name": cl.class_name, "trainer": TrainerData.objects.filter(trainer_id=cl.class_trainer)[0].trainer_name, "stime": cl.class_stime, "etime": cl.class_etime}
            if "Sunday" in days:
                timetable["sunday"][cl.class_id] = {"name": cl.class_name, "trainer": TrainerData.objects.filter(trainer_id=cl.class_trainer)[0].trainer_name, "stime": cl.class_stime, "etime": cl.class_etime}
        except Exception:
            pass
    
    

    params["classes"] = classes_single
    params["timetable"] = timetable
    return render(request, 'website/classes.html', params)



def contact(request):
    return render(request, 'website/contact.html')



def getregistered(request):
    params = {"error":0, "errormessage":"", "success":0, "successmessage": ""}

    if "request" in request.POST:
        name = request.POST.get("name","").title()
        email = request.POST.get("email","").lower()
        contact = request.POST.get("contact","")
        package = request.POST.get("package","")
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        try:
            ad_request = AdmissionData(ad_name=name, ad_email=email, ad_contact=contact, ad_package=package, ad_date=date)
            ad_request.save()
            params["success"] = 1
            params["successmessage"] = "We have recieved your request. Our team will soon contact you regarding the admissions at SmartGYM"
        except Exception:
            params["error"] = 1
            params["errormessage"] = "Something went wrong. Please try again later and if the problem still occurs then contact our admin."
    else:
        if "package_selected" in request.GET:
            package = request.GET.get("package_selected","")
        else:
            package = ""
            

    
    
    params["package"] = package
    return render(request, 'website/memberform.html', params)



def membership(request):
    params = {}
    package_count = PackageData.objects.all().order_by('package_id')
    packages = {}
    for package in package_count:
        features = [feature.lstrip().rstrip() for feature in package.package_features.split(",")]
        packages[package.package_id] = {
                "id":package.package_id, 
                "name": package.package_name, 
                "desc": package.package_desc, 
                "features": features, 
                "price": '{:,}'.format(package.package_price),
                "admission": '{:,}'.format(package.package_admission)
        }
    params["package_list"] = packages 
    return render(request, 'website/membership.html', params)



def trainer(request):
    params = {}
    params["trainers"] = TrainerData.objects.all()
    return render(request, 'website/trainer.html', params)