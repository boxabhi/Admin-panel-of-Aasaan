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




@login_required(login_url='/')
def dashboard(request):

    return render(request , 'dashboard.html')


def show_login_page(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')

    return render(request ,'login.html')



@csrf_exempt
def upload_image(request):
    if request.method == "POST":
        try:
            form = ImageForm(request.POST)
            if form.is_valid():
                image = Image.objects.create(image =form.cleaned_data['image'] )
                image.save()
                user_profile = Profile.objects.get(id = request.user.id)
                user_profile.profile_image = '/media/' + str(image.image)
                user_profile.save()
                image.delete()
                return redirect('/accounts/show/')
        except Exception as e:
            print(e)
    
    return redirect('/accounts/show/')





def show_profile(request):

    context = {}
    try:
        user_profile = User.objects.get(id = request.user.id)
        print(vars(user_profile))
        context['user_profile'] = user_profile
    except Exception as e:
        print(e)
    context['form'] = ImageForm
    print(context)
    return render(request , 'show_profile.html' , context)




def roles(request):
   

    return render(request , 'roles.html')