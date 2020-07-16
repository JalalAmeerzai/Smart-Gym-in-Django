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
