from django.shortcuts import render
from home_app.models import Custom_User

def set_cookies(request,access_code,user_fname,user_sections):
    info_message = {'success_or_danger':'success','strong_text':'Welcome, {}!'.format(user_fname),'info_text':'You have been successfully authorized.'}

    response = render(request,'home.html',{'access_code':access_code,'user_fname':user_fname,'user_sections':user_sections,'info_message':info_message})
    response.set_cookie('access_code',access_code)
    response.set_cookie('user_fname',user_fname)
    return response

def get_cookies(request):
    if 'access_code' in request.COOKIES and 'user_fname' in request.COOKIES:
        access_code = request.COOKIES['access_code']
        user_fname = request.COOKIES['user_fname']
        return access_code,user_fname
    else:
        return '',''

def delete_cookies(request):
    info_message = {'success_or_danger':'success','strong_text':'Successfully Logged Out!'}
    response = render(request,'home.html',{'info_message':info_message})
    if 'access_code' in request.COOKIES and 'user_fname' in request.COOKIES:
        response.delete_cookie('access_code')
        response.delete_cookie('user_fname')
    return response

def get_sections(access_code):
    user_sections = Custom_User.objects.get(access_code=access_code).sections.split(',')
    return user_sections
