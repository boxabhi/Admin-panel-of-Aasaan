import re
from reports.models import Enrollments, FollowUps, Sourcing
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout

from .models import *
from .forms import AddForm, ImageForm
import json
import sys
from reports.helpers import *

import logging
logging.basicConfig()
logger = logging.getLogger(__name__)

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth import get_user_model
User = get_user_model()

from django.contrib.auth.decorators import login_required


class UpdateProfile(APIView):
    def post(self  , request):
        response = {}
        response['status_code'] = 500
        try:
            data = request.data
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            emp_id = data.get('emp_id')
            mobile = data.get('mobile')
            address = data.get('address')
            dob = data.get('dob')
            email = data.get('email')
            
            if is_html(first_name) or is_html(last_name) or is_html(emp_id) or is_html(mobile) or is_html(address):
                response['message'] = 'Not a valid text'
                raise Exception('Not a valid text')

            

            try:
                #user_obj = User.objects.get(id = request.user.id)
                user_obj = Profile.objects.get(id = request.user.id)

                
                # if email and User.objects.filter(email = email).filter():
                #     response['status_code'] = 401
                #     response['message'] =  'Email is taken'
                #     raise Exception('Email is taken')
                # else:
                #     user_obj.email = email
               
                if first_name:
                    user_obj.first_name = first_name
                
                if last_name:
                    user_obj.last_name = last_name

                if emp_id:
                   user_obj.emp_id = emp_id

                if mobile:
                    user_obj.mobile = mobile

                if address:
                    user_obj.address = address

                user_obj.save()
                user_obj.save()

                response['status_code'] = 200
                response['message'] =  'Profile Updated'
            except Exception as e:
                print(e)
                exc_type, exc_obj, exc_tb = sys.exc_info()
                logger.error(f"UpdateProfile {str(e)} at {str(exc_tb.tb_lineno)}")
                response['status_code'] = 401
                response['message'] =  'Something went wrong'


        except Exception as e:
            print(e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error(f"UpdateProfile {str(e)} at {str(exc_tb.tb_lineno)}")
            response['status_code'] = 401
            response['message'] =  'Something went wrong'

        return Response(data =response)


UpdateProfile = UpdateProfile.as_view()


class CreateUser(APIView):
    def post(self  , request):
        response = {}
        response['status_code'] = 500
        response['message'] = 'Something went wrong'        
        try:  
            data = request.data
            data = json.loads(data.get('data'))
            
            print(data)
            if is_html(data.get('email_id')) or is_html(data.get('user_type')) or is_html(data.get('emp_id')):
                response['message'] = 'Not a valid text'
                raise Exception('Not a valid text')
            
            if data.get('email_id') is None or data.get('user_type') is None or data.get('emp_id') is None:
                raise Exception('All field are required')
            
            if Profile.objects.filter(email = data.get('email_id')).first:
                response['message'] = 'A employee exists with this email id'        
                
            if Profile.objects.filter(emp_id = data.get('emp_id')).first:
                response['message'] = 'A employee exists with this emp_id'
                
            profile_obj = Profile.objects.create(
              username=data.get('email_id'),
              email=data.get('email_id'),  
              emp_id=data.get('emp_id'),
              first_name=data.get('first_name'),
              last_name=data.get('last_name'),
              address = data.get('address'),
            ) 
            if int(data.get('user_type')) == 1:
                for role in Role.objects.all():
                    profile_obj.role.add(role)
            else:
                for role in Role.objects.all():
                    profile_obj.role.remove(role)
                
                for role in Role.objects.filter(id__in = data.get('permission')):
                    profile_obj.role.add(role)
        
            profile_obj.set_password(f"ICICI@{data.get('email_id')}")
            
             
            response['status_code'] = 200
            response['message'] = 'User created'
            
        except Exception as e:
            print(e)
            

        return Response(response)
            
CreateUser = CreateUser.as_view()            
        
from rolepermissions.roles import assign_role


class User(APIView):
    def get(self , request):
        response = {}
        response['status_code'] = 500
        response['message'] = 'Something went wrong'        
        try:  
            profile_obj = Profile.objects.get(id = request.GET.get('id'))

            response['data'] = {
                'emp_id' : profile_obj.emp_id,
                'email_id' : profile_obj.email
            }
            

            response['status_code'] = 200
            response['message'] = 'User data'
            
        
        except Exception as e:
            print(e)
        
        return Response(response)


    def post(self, request):
        response = {}
        response['status_code'] = 500
        response['message'] = 'Something went wrong' 
        try:
            data = request.data
            data = json.loads(data.get('data'))
            
            profile_obj = Profile.objects.get(email = data.get('email_id'))
            #{'email_id': 'abhijeet.gupta@allincall.in', 'user_type': '2', 'permission': ['2', '3']}
            
            
            
            if int(data.get('user_type')) == 1:
                assign_role(profile_obj, 'admin')
                for role in Role.objects.all():
                    profile_obj.role.add(role)
            else:
                for role in Role.objects.all():
                    profile_obj.role.remove(role)
                
                for role in Role.objects.filter(id__in = data.get('permission')):
                    profile_obj.role.add(role)
            
            profile_obj.save()
            
            response['status_code'] = 200
            response['message'] = 'Role updated' 
            
            print(data)
        
        except Exception as e: 
            print(e)
        
        return Response(response)
            


User  = User.as_view()


class ToggleActive(APIView):
    def post(self , request):
        response = {}
        response['status_code'] = 500
        response['message'] = 'Something went wrong'
        try:
            data = request.data
            print(data)
            data = json.loads(data.get('data'))
            
            print(id)

            if data.get('id'):
                profile_obj = Profile.objects.get(id = data.get('id'))
                profile_obj.is_active  = not profile_obj.is_active 
                profile_obj.save()
                
                 
            response['status_code'] = 200
            response['message'] = 'User updated'    
            
        except Exception as e: 
            print(e)
            
        return Response(response)       
            
ToggleActive= ToggleActive.as_view()


from src.encrypt import *

class DeleteUser(APIView):
    def post(self, request):
        response = {}
        response['status_code'] = 500
        response['message'] = 'Something went wrong'
        
        try:
            data = request.data
            data = data.get('data')
            
            
            
            if not request.user.profile.role.filter(role_name='delete'):
                raise Exception('You dont have permission')
            
            profile_objs = Profile.objects.filter(id__in = data.get('pk_lists'))
            
            for profile_obj in profile_objs:
                profile_obj.delete()
            
            response['status_code'] = 200
            response['message'] = 'User deleted'
        
        except Exception as e:
            print(e)
            
        return Response(data = response)
            
        
DeleteUser = DeleteUser.as_view()


