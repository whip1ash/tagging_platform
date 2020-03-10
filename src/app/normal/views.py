from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request,'normal/index.html')

def page_not_found(request,exception):
    return render(request,'normal/404.html')

def server_error(request):
    return render(request,'normal/500.html')
