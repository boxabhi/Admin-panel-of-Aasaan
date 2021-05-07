import re
from django.shortcuts import render
from console.constants import isa_id_list , course_id_list , isa_id_dict,course_id_dict
import json
from  console.utils_api import get_upcoming_batch_list
import datetime 
from .helpers import calculates_dates
from newsapp.models import *
from rest_framework.views import APIView
from rest_framework.response import Response
import sys
from .models import *
from reports.models import *
from console.constants import isa_id_list



def home(request):
    context = {'news_objs' : News.objects.all()}
    return render(request , 'home.html' , context)


def home_placement_partners(request):
    #context = {'isa_academy' : isa_id_list}
    context = {'isa_academy' : isa_id_list,'isa_id_list' : isa_id_list  , 'isa_id_dict' : json.dumps(isa_id_dict) , 'course_id_dict' : json.dumps(course_id_dict)}
    
    isa_id = request.GET.get('isa_id')
    course_id = request.GET.get('course_id')
    batch_start_from_date = request.GET.get('batch_start_from_date')
    batch_start_to_date = request.GET.get('batch_start_to_date')
    filter_days = request.GET.get('filter_days')



    try:
        if request.GET:
            print(filter_days)
            if filter_days == 'next_1_months': 
                batch_start_from_date,batch_start_to_date = calculates_dates(30)
            elif filter_days == 'next_2_months': 
                batch_start_from_date,batch_start_to_date = calculates_dates(60)
            elif filter_days == 'next_3_months': 
                batch_start_from_date,batch_start_to_date = calculates_dates(90)
            elif filter_days == 'next_6_months':
                batch_start_from_date,batch_start_to_date = calculates_dates(180)



            if isa_id and course_id and batch_start_from_date and batch_start_to_date:
                payload = get_upcoming_batch_list(isa_id , course_id , batch_start_from_date ,  batch_start_to_date)
                context['courses'] =  payload['details']
                if len(payload['details']) == 0:
                    context['searched'] = True
            context['isa_id'] = isa_id
            context['course_id'] = course_id
            context['batch_start_from_date'] = batch_start_from_date
            context['batch_start_to_date'] = batch_start_to_date
            context['filter_days'] = filter_days
            
            context['checked'] = True
            
    except Exception as e:
        print(e)
        
        
    return render(request , 'home_placement_partners.html' , context)



def batches(request):
    context = {'isa_id_list' : isa_id_list  , 'isa_id_dict' : json.dumps(isa_id_dict) , 'course_id_dict' : json.dumps(course_id_dict)}
    
    isa_id = request.GET.get('isa_id')
    course_id = request.GET.get('course_id')
    batch_start_from_date = request.GET.get('batch_start_from_date')
    batch_start_to_date = request.GET.get('batch_start_to_date')
    filter_days = request.GET.get('filter_days')



    try:
        if request.GET:
            print(filter_days)
            if filter_days == 'next_1_months': 
                batch_start_from_date,batch_start_to_date = calculates_dates(30)
            elif filter_days == 'next_2_months': 
                batch_start_from_date,batch_start_to_date = calculates_dates(60)
            elif filter_days == 'next_3_months': 
                batch_start_from_date,batch_start_to_date = calculates_dates(90)
            elif filter_days == 'next_6_months':
                batch_start_from_date,batch_start_to_date = calculates_dates(180)



            if isa_id and course_id and batch_start_from_date and batch_start_to_date:
                payload = get_upcoming_batch_list(isa_id , course_id , batch_start_from_date ,  batch_start_to_date)
                context['courses'] =  payload['details']
                if len(payload['details']) == 0:
                    context['searched'] = True
            context['isa_id'] = isa_id
            context['course_id'] = course_id
            context['batch_start_from_date'] = batch_start_from_date
            context['batch_start_to_date'] = batch_start_to_date
            context['filter_days'] = filter_days

    except Exception as e:
        print(e)





    return render(request , 'home_batches.html' , context)




def verify_ceriticate(request):
    context = {}
    if request.GET.get('certificate_id'):
        certificate_obj = Certificate.objects.filter(certificate_id = request.GET.get('certificate_id')).first()
        if certificate_obj:
            context = {'certificate_obj' : certificate_obj , 'is_found' :True , 'is_searched' : True}
        else:
            context = {'is_found' : False , 'is_searched' : True}

    print(context)
    return render(request , 'verify_certificate.html'  , context)



class CreatePlacementPartners(APIView):


    def post(self , request):
        response = {}
        response['status_code'] = 500
        response['message'] = 'Something went wrong'
        try:
            data = request.data
            print(data)
            name_of_the_company  = data.get('name_of_company')
            address_detail  = data.get('address_detail')
            city  = data.get('city')
            state  = data.get('state')
            name_of_person  = data.get('name_of_person')
            designation_of_person  = data.get('designation_of_person')
            mobile_number  = data.get('mobile_number')
            email  = data.get('email')
            type_of_company  = data.get('type_of_company')
            others_div = data.get('others_div')

            PlacementPartners.objects.create(
                name_of_the_company  = name_of_the_company,
                    address_detail = address_detail,
                    city = city,
                    state = state,
                    name_of_person = name_of_person,
                    designation_of_person = designation_of_person,
                    mobile_number = mobile_number,
                    email = email,
                    type_of_company = type_of_company + ' - ' + others_div
            )

            response['status_code'] = 200
            response['message'] = 'Your response has been recorded'


        except Exception as e:
            print(e)
            

        return Response(response)

CreatePlacementPartners = CreatePlacementPartners.as_view()



class CreateScheduleInterview(APIView):
    def post(self , request):
        response = {}
        response['status_code'] = 500
        response['message'] = 'Something went wrong'
        try:
            data = request.data

            RequirementPlacementPartner.objects.create(
              name_of_company  = data.get('name_of_company'),
                location  = data.get('location'),
                course  = data.get('course'),
                designation  = data.get('designation'),
                salary  = data.get('salary'),
                contact_person  = data.get('contact_person'),
                job_text  = data.get('job_text'),
                job_description_file  = data.get('job_description_file'),
                no_of_opening  = data.get('no_of_opening'),

            )
            response['status_code'] = 200
            response['message'] = 'We will get back to you'
        
        except Exception as e:
            print(e)

        return Response(response)


CreateScheduleInterview = CreateScheduleInterview.as_view()


class CreateTreePlantation(APIView):
    def post(self , request):
        response = {}
        response['status_code'] = 500
        response['message'] = 'Something went wrong'

        try:
            data = request.data
            # print(data)
            # print(request.FILES)
            # print('FILES ))))))')
            # print(request.FILES.getlist('images'))
            
            # return Response(response)
           

            date_of_plantation   = data.get('date_of_plantation')
            isa_location  = data.get('isa_location')
            no_of_trees  = data.get('no_of_trees')
            varieties  = data.get('varieties')
            occasion  = data.get('occasion')
            parternship  = data.get('parternship')
            staff  = data.get('staff')
            post_plantation_care_by  = data.get('post_plantation_care_by')



            tree_plantation_obj = TreePlantation.objects.create(
                date_of_plantation  = date_of_plantation,
                isa_location  = isa_location,
                no_of_trees  = no_of_trees,
                varieties  = varieties,
                occasion  = occasion,
                parternship  = parternship,
                staff  = staff,
                post_plantation_care_by  = post_plantation_care_by,
            )
            images = request.FILES.getlist('images')

        
            try:
                for image in images:
                    TreePlantationPhotos.objects.create(
                        tree_plantation=tree_plantation_obj,
                        file = image
                    )
            except Exception as e:
                print('@@@')
                print(e)
                print('@@@')



            response['status_code'] = 200
            response['message'] = 'Tree Plantation created'
        
        except Exception as e:

            print(e)

        return Response(response)

CreateTreePlantation = CreateTreePlantation.as_view()



class CreateWatershedData(APIView):
    def post(self , request):
        response = {}
        response['status_code'] = 500
        response['message'] = 'Something went wrong'

        try:
            data = request.data
            date   = data.get('date')
            name_of_school  = data.get('name_of_school')
            name_of_village  = data.get('name_of_village')
            block  = data.get('block')
            district  = data.get('district')
            terrace  = data.get('terrace')
            reservoir_type  = data.get('reservoir_type')

            water_shed_data__obj = WatershedData.objects.create(
                date  = date,
                name_of_school = name_of_school,
                name_of_village = name_of_village,
                block = block,
                district = district,
                terrace = terrace,
                reservoir_type = reservoir_type,
            )
            images = request.FILES.getlist('images')

        
            try:
                for image in images:
                    WatershedDataPhotos.objects.create(
                        water_shed_data=water_shed_data__obj,
                        file = image)
            except Exception as e:
                print(e)

            response['status_code'] = 200
            response['message'] = 'CreateWatershedData  created'
        
        except Exception as e:

            print(e)

        return Response(response)

CreateWatershedData = CreateWatershedData.as_view()


class AddRemarks(APIView):
    def post(self , request):
        response = {}
        response['status_code'] = 500
        response['message'] = 'Something went wrong'

        try:
            data = request.data

            id = data.get('id')
            address_remarks = data.get('address_remarks')

            placement_obj = PlacementPartners.objects.get(id = id)
            placement_obj.address_remarks = address_remarks
            placement_obj.is_addressed = True
            placement_obj.addressed_by = request.user
            placement_obj.save()

            response['status_code'] = 200
            response['message'] = 'Remarks added'


        
        except Exception as e:
            print(e)
        
        return Response(response)

AddRemarks = AddRemarks.as_view()

