from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
# Create your views here.

def home(request):
    return render(request, 'home.html',{'name':'vaibhav'})



def add(request):
    value1 = int(request.POST['name1'])
    value2 = int(request.POST['name2'])
    res = value1 + value2
    return render(request, "result.html" , {'result': res})
