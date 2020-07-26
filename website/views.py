from django.shortcuts import render
from django.http import HttpResponse
from adminportal.models import ClassData, TrainerData

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
    return render(request, 'website/memberform.html')



def membership(request):
    return render(request, 'website/membership.html')



def trainer(request):
    return render(request, 'website/trainer.html')