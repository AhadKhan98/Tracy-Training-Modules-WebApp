from django.shortcuts import render
from home_app.models import Custom_User

# Create your views here.
def home(request):
    if request.method == 'POST':
        post_data = dict(request.POST)
        access_code = post_data['access_code'][0]
        print('ACCESS CODE: ' + access_code)
        return render(request,'home.html',{access_code:access_code})
    return render(request,'home.html')

def login(request):
    all_users = Custom_User.objects.all()
    all_access_codes = []
    for user in all_users:
        all_access_codes += [user.access_code]
    return render(request,'login.html',{'all_access_codes':all_access_codes})

def register(request):
    return render(request,'register.html')

def module(request):
    return render(request,'module.html')

def quiz(request):
    return render(request,'quiz.html')
