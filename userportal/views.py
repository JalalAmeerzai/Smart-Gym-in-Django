from django.shortcuts import render, redirect
from django.http import HttpResponse

def login(request):
    if request.method == 'POST':
        return redirect('/userportal/user/')
    return render(request, 'userportal/login.html')



def passwordlost(request):
    return render(request, 'userportal/lost-password.html')




def userprofile(request):
    return render(request, 'userportal/user.html')



def settings(request):
    return render(request, 'userportal/settings.html')



def routines(request):
    return render(request, 'userportal/routine.html')



def createroutines(request):
    return render(request, 'userportal/createroutine.html')




def viewroutine(request):
    return render(request, 'userportal/routineview.html')



def diet(request):
    return render(request, 'userportal/diet.html')



def exercises(request):
    return render(request, 'userportal/exercise.html')



def finances(request):
    return render(request, 'userportal/finances.html')



def help(request):
    return render(request, 'userportal/help.html')



def subscription(request):
    return render(request, 'userportal/subscription.html')
