from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,'home.html')

def login(request):
    return render(request,'login.html')

def register(request):
    return render(request,'register.html')

def module(request):
    return render(request,'module.html')

def quiz(request):
    return render(request,'quiz.html')
