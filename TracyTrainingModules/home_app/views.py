from django.shortcuts import render
from home_app.models import Custom_User
import random,string

# Create your views here.
def home(request):
    all_users = Custom_User.objects.all()
    all_access_codes = []
    for user in all_users:
        all_access_codes += [user.access_code]


    def generate_access_code():
        # Getting all previously stored access codes from the database.
        all_characters = string.ascii_letters + string.digits
        access_code = "".join([random.choice(all_characters) for x in range(25)])
        if access_code in all_access_codes:
            generate_access_code()
        return access_code

    if request.method == 'POST':
        if 'access_code' in request.POST: # Coming from login.html
            access_code = request.POST['access_code']
            user_fname = Custom_User.objects.get(access_code=access_code).first_name
            return render(request,'home.html',{'access_code':access_code,'user_fname':user_fname})
        elif 'first_name' in request.POST: # Coming from register.html
            first_name,last_name,email = request.POST['first_name'],request.POST['last_name'],request.POST['email']
            access_code = generate_access_code()

            user = Custom_User(access_code=access_code,user_type='sup',first_name=first_name,last_name=last_name,email=email,sections='1,0,0,0,0,0,0,0,0,0,0')
            user.save()
            print('saved to database')
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
