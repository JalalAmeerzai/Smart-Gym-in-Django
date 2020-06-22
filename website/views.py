from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, 'website/index.html')



def classes(request):
    return render(request, 'website/classes.html')



def contact(request):
    return render(request, 'website/contact.html')



def getregistered(request):
    return render(request, 'website/memberform.html')



def membership(request):
    return render(request, 'website/membership.html')



def trainer(request):
    return render(request, 'website/trainer.html')