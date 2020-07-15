from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
#from django.views.decorators.csrf import csrf_exempt
#import json
#import base64

def index(request):
    return render(request, 'index.html')

#@csrf_exempt
#def productapi(request):
    #if request.method=="POST":
        #jalal = [{'id':'existing','name':'test user'}]
        #jalal.append({'id': request.GET.get('id', ''), 'name': request.GET.get('name', '')})
        #products = Product.objects.all()
        #return HttpResponse(json.dumps(jalal,  default=str))
        
        
        #objectreturn = {}
        #for i in range(1,4):
            #obj = "obj"+str(i)
            #objectreturn[obj] = {"id": i, "name": "test"+str(i)}
        #objectreturn["obj"+str(request.POST.get('id', ''))] = {'id': request.POST.get('id', ''), 'name': json.loads(request.POST.get('name', ''))}
        
        #imgstr = request.POST.get('image', '')
        #image_64_decode = base64.decodebytes(imgstr.encode('ascii'))
        #image_result = open('cv233.png', 'wb') # create a writable image and write the decoding result
        #image_result.write(image_64_decode)

        #converting string to json
        #y = json.loads(request.POST.get('name', ''))
        #print(y["obj1"])
        #return JsonResponse(objectreturn) 