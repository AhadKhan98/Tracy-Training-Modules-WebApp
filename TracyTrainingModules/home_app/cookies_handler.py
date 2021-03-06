from django.shortcuts import render
from home_app.models import Custom_User,Content
from django.http import HttpResponseRedirect
from django.urls import reverse

def set_cookies(request,access_code,user_fname,user_sections,sections_and_modules):
    info_message = {'success_or_danger':'success','strong_text':'Welcome, {}!'.format(user_fname),'info_text':'You have been successfully authorized.'}
    
    response = HttpResponseRedirect(reverse('home'))
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

def get_sections_range(show_to='all'):
    all_content_list = list(Content.objects.filter(show_to=show_to))
    all_content_list = list(map(str,all_content_list))
    sections_and_modules = {}
    for content in all_content_list:
        colon_idx = content.index(':')
        space_idx = content.index(' ')
        current_section_num = int(content[colon_idx+1:space_idx])
        if current_section_num not in sections_and_modules:
            sections_and_modules[current_section_num] = 1
        else:
            sections_and_modules[current_section_num] += 1
    return sections_and_modules

def update_sections_by_user_type(request,sections_and_modules):
    access_code,user_fname = get_cookies(request)
    if access_code:
        current_user_type = Custom_User.objects.get(access_code=access_code).user_type
        sections_by_user_type = get_sections_range(current_user_type)
        sections_by_user_type.update(sections_and_modules)
        sections_and_modules = sections_by_user_type
    return sections_and_modules
