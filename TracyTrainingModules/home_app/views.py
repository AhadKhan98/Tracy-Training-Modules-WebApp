import mimetypes
import os
import random
import string

from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse

from home_app.certificate_handler.certificate_handler import *
from home_app.cookies_handler import *
from home_app.models import Content, Custom_User


def home(request):

    # Gets list of all available sections and modules
    sections_and_modules = get_sections_range()
    sections_and_modules = update_sections_by_user_type(request,sections_and_modules)


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
            # In case of an invalid access code
            if access_code not in all_access_codes:
                info_message = {'success_or_danger':'danger','strong_text':'Invalid Access Code!','info_text':'Please enter a valid access code. If you don\'t have a code, register below and a new code will be e-mailed to you.'}
                return render(request,'login.html',{'info_message':info_message,})
            user_fname = Custom_User.objects.get(access_code=access_code).first_name
            user_sections = get_sections(access_code)
            return set_cookies(request,access_code,user_fname,user_sections,sections_and_modules) # Loads homepage and sets cookies for logged in user

        elif 'first_name' in request.POST: # Coming from register.html
            user_fname,user_lname,email,user_type = request.POST['first_name'],request.POST['last_name'],request.POST['email'],request.POST['user_type']
            default_sections = ''
            if user_type == 'Student':
                user_type = 'stu'
                default_sections = '1,0,0,0,0,0,0,0,0,0,0'
            else:
                user_type = 'sup'
                default_sections = '1,1,0,0,0,0,0,0,0,0,0'
            access_code = generate_access_code()
            user = Custom_User(access_code=access_code,user_type=user_type,first_name=user_fname,last_name=user_lname,email=email,sections=default_sections)
            user.save()
            user_sections = get_sections(access_code)
            # Send e-mail to newly registered user
            # email_body = '''Hi {}!\n\nThank you for signing up to the Berea College Labor Program\'s Tracy Training Modules.\nHere is your access code: {}\n\nPlease use the provided code to login to the website. If you have any questions, feel free to send us an email.\n\nBest Regards,\nThe Labor Program Team'''.format(user_fname,access_code)
            # send_mail('Tracy Training Modules Access Code',email_body,'iahadkhan98@gmail.com',[email],fail_silently=False)
            return set_cookies(request,access_code,user_fname,user_sections,sections_and_modules)

    else: # GET Method

        access_code,user_fname = get_cookies(request)
        if access_code != '':
            user_sections = get_sections(access_code)

            referer = request.META.get('HTTP_REFERER')
            if referer is not None and 'section' in referer and 'quiz' in referer:
                sec_num = referer[referer.index('n')+1:referer.index('-')]
                info_message = {'success_or_danger':'success','strong_text':'Success!','info_text':'Section {} has been successfully unlocked.'.format(int(sec_num)+1)}
                if sec_num == '10':
                    return HttpResponseRedirect(reverse('completion'))

                return render(request,'home.html',{'access_code':access_code,'user_fname':user_fname,'user_sections':user_sections,'info_message':info_message,'section_range':sections_and_modules})

            return render(request,'home.html',{'access_code':access_code,'user_fname':user_fname,'user_sections':user_sections,'section_range':sections_and_modules})

        else:
            return render(request,'home.html',{'access_code':access_code,'user_fname':user_fname,'section_range':sections_and_modules})


def login(request):
    all_users = Custom_User.objects.all()
    all_access_codes = []
    for user in all_users:
        all_access_codes += [user.access_code]
    return render(request,'login.html')

def logout(request):
    response = delete_cookies(request)
    return response

def register(request):
    access_code,user_fname = get_cookies(request)
    return render(request,'register.html',{'access_code':access_code,'user_fname':user_fname})

def module(request,sec_num,module_num):

    sections_and_modules = get_sections_range()
    sections_and_modules = update_sections_by_user_type(request,sections_and_modules)

    access_code,user_fname = get_cookies(request)
    if access_code != '':
        user_sections = get_sections(access_code)
        if user_sections[sec_num-1] == '1':
            content = Content.objects.filter(section_num=sec_num,module_num=module_num)
            if len(content) != 0:
                content = content[0]
                return render(request,'module.html',{'access_code':access_code,'user_fname':user_fname,'user_sections':user_sections,'content':content,'section_range':sections_and_modules})
            else:
                return render(request,'module.html',{'access_code':access_code,'user_fname':user_fname,'user_sections':user_sections,'section_range':sections_and_modules})
    else:
        return render(request,'access_denied.html',{'access_code':access_code,'user_fname':user_fname,'section_range':sections_and_modules})

def quiz(request,sec_num):
    sections_and_modules = get_sections_range()
    sections_and_modules = update_sections_by_user_type(request,sections_and_modules)

    access_code,user_fname = get_cookies(request)
    if access_code != '':
        user_sections = get_sections(access_code)
        if user_sections[sec_num] == '1':
            return render(request,'quiz.html',{'access_code':access_code,'user_fname':user_fname,'user_sections':user_sections,'sec_num':sec_num,'section_range':sections_and_modules})
        else:
            return render(request,'access_denied.html',{'access_code':access_code,'user_fname':user_fname,'user_sections':user_sections,'section_range':sections_and_modules})
    else:
        return render(request,'access_denied.html',{'access_code':access_code,'user_fname':user_fname,'section_range':sections_and_modules})

def enable_next_section_and_redirect(request,sec_num):
    sections_and_modules = get_sections_range()
    sections_and_modules = update_sections_by_user_type(request,sections_and_modules)
    num_of_sections = len(get_sections_range())
    access_code,user_fname = get_cookies(request)
    user_sections = get_sections(access_code)
    if sec_num == num_of_sections:
        return HttpResponseRedirect(reverse('home'))
    user_sections[sec_num+1] = '1'
    updated_sections = ",".join(user_sections)
    usr = Custom_User.objects.get(access_code=access_code)
    usr.sections = updated_sections
    usr.save()
    return HttpResponseRedirect(reverse('home'))

def completion(request):
    access_code,user_fname = get_cookies(request)
    usr = Custom_User.objects.get(access_code=access_code)
    if access_code != '':
        formatted_fullname = '{} {}'.format(user_fname.split(' ')[0], usr.last_name.split(' ')[0])
        generate_certificate(formatted_fullname, access_code)
        user_sections = get_sections(access_code)
    sections_and_modules = get_sections_range()
    sections_and_modules = update_sections_by_user_type(request,sections_and_modules)
    usr = Custom_User.objects.get(access_code=access_code)
    print(usr.last_name)
    usr_email = usr.email
    return render(request,'completion.html',{'usr_email':usr_email, 'access_code':access_code, 'user_fname':user_fname,'user_sections':user_sections,'section_range':sections_and_modules})

def download_certificate(request, access_code):
    file_path = os.path.join(settings.BASE_DIR,'home_app/certificate_handler/{}.pdf'.format(access_code))
    mime_type, _ = mimetypes.guess_type(file_path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type=mime_type)
            response['Content-Disposition'] = 'inline; filename={}'.format(file_path)
            return response
    raise Http404
