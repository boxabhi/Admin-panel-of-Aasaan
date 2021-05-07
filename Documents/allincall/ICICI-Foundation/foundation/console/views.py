import re
from django.shortcuts import render, redirect
from django.http import HttpResponse, response
import datetime

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .utils_api import *
from reports.models import *
from .helpers import *
import sys
from newsapp.models import News

from accounts.models import Profile

import logging
logging.basicConfig()
logger = logging.getLogger(__name__)


from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.


import io
import os




def dashboard(request):
    data = [Sourcing.objects.all().count(), Enrollments.objects.all().count(),FollowUps.objects.all().count()]
      
    context = {}
    context['data'] = data
    context['is_active'] ='dashboard' 
    context['news'] = News.objects.all()
    context['impact_box'] = ImpactBox.objects.first()
    context['birthdays'] = get_birth_days()
    # print(get_birth_days())
    return render(request , 'dashboard.html',  context)

def Home(request):
    context = {}
    
    if request.user.is_authenticated:
        return redirect('/dashboard')

        #return render(request, 'console/index.html', context)
    
    context['is_active'] ='home' 
    
    return redirect('/accounts/login')


def show_reports(request):
    context = {}
    try:
        sourcing_reports_objs = SourcingReportStatus.objects.all()

    except Exception as e:
        pass 
    context['is_active'] ='show_reports' 
    
    return render(request , 'console/reports.html' , context)









class LoginAPI(APIView):

    def post(self , request):
        response = {}
        response['status_code'] = 500

        try:
            request_type = request.GET.get('type')
            data = request.data
            print(request.data)
            username = data.get('username')
            password = data.get('password')

            user = Profile.objects.filter(email = data.get('username')).first()
            login(request , user)

            if request_type == 'google': 
                # if not check_valid_email(data.get('email')):
                #     response['message'] = "Permission denied"
                #     response['status_code'] = 401
                #     raise Exception('not authorized')
            
                user = Profile.objects.filter(email = data.get('email')).first()
                login(request , user)
                
                if user:
                    login(request , user)
                    user.profile_image = data.get('img')
                    user.save()
                    response['message'] = "Welcome"
                    response['status_code'] = 200
                    return Response(data = response)

                else: 
                    name = data.get('name')
                    first_name = None
                    last_name = None
                    if name:
                        name = name.split(' ')
                        if len(name) == 2:
                            first_name = name[0]
                            last_name = name[1]
                        else:
                            first_name = name[0]

                    user = Profile.objects.create(profile_image=data.get('img') , email = data.get('email'), username=data.get('email') , first_name = first_name , last_name=last_name)
                    login(request , user)
                    response['message'] = "Welcome"
                    response['status_code'] = 200
                    return Response(data = response)
            


            if username is  None or  password is None:
                response['status_code'] =  400
                response['message'] = "Both username & password are required"
                raise Exception("Both username & password are required")


            user = Profile.objects.filter(username = username).first()
            if user is None:
                response['message'] = "Username not found"
                response['status_code'] = 400
                raise Exception("Username not found")


            check_user = authenticate(username = username , password = password)

            if check_user:
                response['message'] = "Welcome"
                response['status_code'] = 200
                login( request , user)
                print(user)
            else:
                response['message'] = "Incorrect password"
                response['status'] = 400
                raise Exception("Incorrect password")


        
        except Exception as e :
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("LoginAPI %s at %s",
                         str(e), str(exc_tb.tb_lineno))

        
        return Response(data = response)


LoginAPI = LoginAPI.as_view()




def logout_user(request):
    logout(request)
    return response.JsonResponse({'status_code' : 200})
