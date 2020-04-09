from django.shortcuts import render
from home_app.models import Custom_User
from home_app.cookies_handler import *
import random,string


def home(request):

    # Gives global access to all access codes stored in the database
    all_users = Custom_User.objects.all()
    all_access_codes = []
    for user in all_users:
        all_access_codes += [user.access_code]


    def generate_access_code():
        """ This function randomly generates an access code and makes sure it is not duplicated in the database. """
        all_characters = string.ascii_letters + string.digits
        access_code = "".join([random.choice(all_characters) for x in range(25)])
        if access_code in all_access_codes:
            generate_access_code()
        return access_code

    if request.method == 'POST': # POST Method

        if 'access_code' in request.POST: # Coming from login.html
            access_code = request.POST['access_code']
            user_fname = Custom_User.objects.get(access_code=access_code).first_name
            user_sections = get_sections(access_code)
            return set_cookies(request,access_code,user_fname,user_sections) # Loads homepage and sets cookies for logged in user

        elif 'first_name' in request.POST: # Coming from register.html
            user_fname,user_lname,email = request.POST['first_name'],request.POST['last_name'],request.POST['email']
            access_code = generate_access_code()
            user = Custom_User(access_code=access_code,user_type='sup',first_name=user_fname,last_name=user_lname,email=email,sections='1,0,0,0,0,0,0,0,0,0,0')
            user.save()
            user_sections = get_sections(access_code)
            return set_cookies(request,access_code,user_fname,user_sections)

    else: # GET Method

        access_code,user_fname = get_cookies(request)
        if access_code != '':
            user_sections = get_sections(access_code)
            return render(request,'home.html',{'access_code':access_code,'user_fname':user_fname,'user_sections':user_sections})
        else:
            return render(request,'home.html',{'access_code':access_code,'user_fname':user_fname})


def login(request):
    all_users = Custom_User.objects.all()
    all_access_codes = []
    for user in all_users:
        all_access_codes += [user.access_code]
    return render(request,'login.html',{'all_access_codes':all_access_codes})

def logout(request):
    response = delete_cookies(request)
    return response

def register(request):
    access_code,user_fname = get_cookies(request)
    return render(request,'register.html',{'access_code':access_code,'user_fname':user_fname})

def module(request,sec_num,module_num):
    access_code,user_fname = get_cookies(request)
    if access_code != '':
        user_sections = get_sections(access_code)
        if user_sections[sec_num-1] == '1':
            return render(request,'module.html',{'access_code':access_code,'user_fname':user_fname,'user_sections':user_sections,'sec_num':sec_num,'module_num':module_num})
        else:
            return render(request,'access_denied.html',{'access_code':access_code,'user_fname':user_fname,'user_sections':user_sections})
    else:
        return render(request,'access_denied.html',{'access_code':access_code,'user_fname':user_fname})

def quiz(request,sec_num):
    access_code,user_fname = get_cookies(request)
    if access_code != '':
        user_sections = get_sections(access_code)
        if user_sections[sec_num-1] == '1':
            return render(request,'quiz.html',{'access_code':access_code,'user_fname':user_fname,'user_sections':user_sections,'sec_num':sec_num})
        else:
            return render(request,'access_denied.html',{'access_code':access_code,'user_fname':user_fname,'user_sections':user_sections})
    else:
        return render(request,'access_denied.html',{'access_code':access_code,'user_fname':user_fname})
