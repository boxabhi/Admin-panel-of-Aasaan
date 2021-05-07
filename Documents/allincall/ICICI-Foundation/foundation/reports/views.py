from django import contrib
from django.core.checks.messages import Info
from django.db import reset_queries
from django.http import response
from django.shortcuts import redirect, render
from .models import Sourcing
from rest_framework.views import APIView
from rest_framework.response import Response
import sys
import xlrd
import logging
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from .utils import *
from .cron import *
from django.core.exceptions import PermissionDenied
from  console.utils_api import get_batch_data , get_batch_details ,get_custom_enrolled_trainee
from accounts.models import *
from console.models import *
from django.http import HttpResponseForbidden
from accounts.auth import *
from django.utils.dateparse import parse_date
import datetime
import os
from console.constants import isa_id_list

from home.models import *

logging.basicConfig()
logger = logging.getLogger(__name__)

from rest_framework import permissions


BASE_DIR = settings.BASE_DIR

from rolepermissions.roles import get_user_roles,assign_role
#from rolepermissions.decorators import has_permission_decorator,has_role_decorator
from rolepermissions.checkers import has_permission
from src.encrypt import *
from rolepermissions.permissions import available_perm_status
from src.roles import has_permission_checker


def show_users(request):
    #has_permission_checker('can_view_users' , request)


    context = {'is_active' : 'users'}
    user_objs = Profile.objects.all()
    context['user_objs'] = user_objs
    context['roles'] = Role.objects.all()
    return render(request , 'users.html' , context)



def referral(request):
    has_permission_checker('can_view_reffral' , request)

    context = {'is_active' : 'referral'}
    refrral_objs = Referral.objects.all()
    try:
        if request.GET:
            if 'start_date' in request.GET and 'end_date' in request.GET:
                start_date = datetime.datetime.strptime(request.GET.get('start_date'), "%Y-%m-%d").date()
                end_date = datetime.datetime.strptime(request.GET.get('end_date'), "%Y-%m-%d").date()
                refrral_objs = refrral_objs.filter(created_at__range=[start_date, end_date])

            if 'specific_filter' in request.GET:
                print('called')
                refrral_objs = refrral_objs.filter(referrer_name__icontains=request.GET.get('specific_filter')) | refrral_objs.filter(referrer_mobile__icontains=request.GET.get('specific_filter')) | refrral_objs.filter(referrer_email__icontains=request.GET.get('specific_filter')) | refrral_objs.filter(referee_name__icontains=request.GET.get('specific_filter')) |  refrral_objs.filter(referee_mobile__icontains=request.GET.get('specific_filter')) |  refrral_objs.filter(referee_email__icontains=request.GET.get('specific_filter')) |  refrral_objs.filter(source__icontains=request.GET.get('specific_filter'))

            if 'days_filter' in request.GET:
                days = request.GET.get('days')
                refrral_objs = refrral_objs.filter(created_at__lte=datetime.datetime.today(), create_ate__gt=datetime.datetime.today()-datetime.timedelta(days=days))
            context['start_date'] = request.GET.get('start_date')
            context['end_date'] = request.GET.get('end_date')
            
    except Exception as e:
        print(e)
        
    
    graph_obj = []
    dates_objs = []
    set_of_dates = set()
    for refrral_obj in refrral_objs:
        set_of_dates.add(str(refrral_obj.created_at)[0:9])
        dates_objs.append(str(refrral_obj.created_at)[0:9])
        dates_objs.sort()
    for date in set_of_dates:    
        graph_obj.append({
                    'date' : date,
                    'count' : dates_objs.count(date)
        })
            
    dates = []
    frequency = []
            
    for graph in graph_obj:
        dates.append(str(graph['date']))
        frequency.append(graph['count'])
                
    context['graph_obj'] = json.dumps(graph_obj)
    context['dates'] = json.dumps(dates)
    context['frequency'] = json.dumps(frequency)

    context['referral_objs'] = refrral_objs
    #print(context)
    return render(request , 'referral.html' , context)


def batches(request):
    has_permission_checker('can_view_batches' , request)

    context = {'is_active' : 'batches'}
    
    if request.GET.get('emp_id'):
        emp_id = request.GET.get('emp_id')
        data = get_batch_details(emp_id)
        payload = []
        for data in data['details']:
            temp = data
            temp['is_stored'] = False
            temp['students'] = 'N/A'
                
            if Batch.objects.filter(batch_id=temp['BatchId']).first():
                   
                temp['students'] = len(Trainee.objects.filter(batch_id=temp['BatchId']))
                temp['is_stored'] = True
            payload.append(temp)                
        
            
        payload.sort(key=lambda x:x['BatchEndDate'])
            
        payload.reverse()
        context['datas'] = payload

    return render(request , 'batches.html', context )


def students(request , batch_id):
    context = {
        'batch_id' : batch_id,
        'is_active' : 'batches',
        'certificate_template_objs' : CertificateTemplates.objects.all()
        }
        
    datas = get_batch_data(batch_id)
    payload = []
    for data in datas['details']:
        name = str(data['TraineeName'])
        data['TraineeName'] = (name.split('-'))[1]
        data['is_certificate_issued'] = False
        trainee_obj =  Trainee.objects.filter(trainee_id=data['TraineeId']).first()
        
        if trainee_obj:
            if trainee_obj.is_certificate_issued:
                data['is_certificate_issued'] = True
            data['is_stored'] = True
        else:
            data['is_stored'] = False
        
        payload.append(data)
    context['datas'] = payload
    context['is_active'] ='batches' 
    return render(request , 'students.html', context )




def sourcing(request):
    has_permission_checker('can_view_sourcing' , request)

    context = {}
    sourcing_reports_objs = SourcingReportStatus.objects.filter(is_visible=True , user=request.user)
    context['sourcing_reports_objs'] = sourcing_reports_objs
    context['is_active'] ='reports' 
    return render(request , 'options/sourcing.html', context )


def enrollments(request):
    has_permission_checker('can_view_enrollments' , request)

    context = {}
    enrollment_report_objs = EnrollmentReportStatus.objects.filter(is_visible=True , user = request.user) 
    context['enrollment_report_objs'] = enrollment_report_objs
    context['is_active'] ='reports' 
    return render(request , 'options/enrollments.html', context )
 


def followups(request):
    has_permission_checker('can_view_followups' , request)

    context = {}
    follow_up_report_objs = FollowUpsReportStatus.objects.filter(is_visible=True , user = request.user)
    context['follow_up_report_objs'] = follow_up_report_objs
    context['is_active'] ='reports' 
    return render(request , 'options/followups.html', context )



def remove_upload_user(request , id):
    has_permission_checker('can_manage_users' , request)

    context = {}
    try:
        user_upload_objs = UserUploadExcel.objects.get(id = id)
        user_upload_objs.delete()
        context['is_active'] ='users'
        print(context)
    except Exception as e:
        print(e)
    return redirect('/reports/upload-users/')

def upload_user_excel(request):
    has_permission_checker('can_manage_users' , request)

    context = {}
    context['user_upload_objs'] = UserUploadExcel.objects.all()
    context['is_active'] ='users'
    return render(request , 'upload_users.html', context )
     
    

def views_enrollments(request , id):
    has_permission_checker('can_view_enrollments' , request)
    
    context = {}
    try:
        enrollment_report_obj = EnrollmentReportStatus.objects.get(id = id)

        if enrollment_report_obj.user != request.user:
            raise PermissionDenied

        enrollments = Enrollments.objects.filter(enrollment_report = enrollment_report_obj)
        context['enrollments'] = enrollments
        context['enrollment_report_obj'] = enrollment_report_obj
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.error(f"Trigger {str(e)} at {str(exc_tb.tb_lineno)}")

    print(context)
    context['is_active'] ='reports' 
    
    return render(request ,'views_enrollments.html' , context)


def views_sourcing(request , id):
    has_permission_checker('can_view_sourcing' , request)

    context = {}
    try:
        sourcing_report_obj = SourcingReportStatus.objects.get(id = id)
        if sourcing_report_obj.user != request.user:
            raise PermissionDenied

        sourcings = Sourcing.objects.filter(sourcing_report = sourcing_report_obj)
        context['sourcings'] = sourcings
        context['sourcing_report_obj'] = sourcing_report_obj
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.error(f"Trigger {str(e)} at {str(exc_tb.tb_lineno)}")

    context['is_active'] ='reports'  
    
    return render(request ,'views_sourcing.html' , context)


def views_followups(request , id):
    has_permission_checker('can_view_followups' , request)

    context = {}
    try:
        followps_report_obj = FollowUpsReportStatus.objects.get(id = id)

        if followps_report_obj.user != request.user:
            raise PermissionDenied

        followps = FollowUps.objects.filter(follow_up_report = followps_report_obj)
        context['followps'] = followps
        context['followps_report_obj'] = followps_report_obj
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.error(f"Trigger {str(e)} at {str(exc_tb.tb_lineno)}")

    print(context)
    context['is_active'] ='reports'  
    
    return render(request ,'views_follow.html' , context)








def assigned_followups(request):
    context = {'isa_id_list' : isa_id_list}

    response = None
    if request.GET:
        isa_id = request.GET.get('isa_id')
        from_batch_start_date =request.GET.get('from_batch_end_date')
        to_batch_end_date =request.GET.get('from_batch_end_date')
        response = get_custom_enrolled_trainee(isa_id, from_batch_start_date , to_batch_end_date)
        
        datas = []
        for data in response['details']:
            temp = str(data['TraineeName'])
            temp = temp.split('-')
            data['ApplicantId'] = temp[0]
            data['TraineeName'] = temp[1]
            datas.append(data)
        context['datas'] = datas

    context['users'] = Profile.objects.all()

    return render(request , 'assigned_followups.html' , context)



def manage_followups(request):

    
    context = {}
    context['is_active'] = 'followups'
    
    try:
        user_batch_followups_obj = UserBatchFollowups.objects.filter(assign_to_user= request.user)
        context['user_batch_followups_obj'] = user_batch_followups_obj
    except Exception as e:
        print(e)
    
    print(context)
    return render(request ,'manage_followups.html' , context)


def view_assigned_followups(request):
    has_permission_checker('can_view_followups' , request)

    context = {}
    context['is_active'] = 'followups'

    user_batch_followups = UserBatchFollowups.objects.all()
    
    context['batchfollowupsrecord'] = UserBatchFollowups.objects.all()
    context['time'] = datetime.datetime.now()
    return render(request ,'view_assigned_followups.html' , context)

def show_assigned_followups(request , id):
    context = {}
    context['is_active'] = 'followups'
    try:
        user_batch_follow_ups = UserBatchFollowups.objects.get(id =id)
        if not check_admin_user(request.user) and request.user != user_batch_follow_ups.assign_to_user:
            return HttpResponseForbidden()

        context['datas'] =  user_batch_follow_ups.batch_followups.all()
    except Exception as e:
        print(e)
    return render(request ,'show_assigned_followups.html' , context)




def placement_partners(request):
    context = {'placement_partners_objs' : PlacementPartners.objects.all() , 'is_active' : 'placement_partners'}
    return render(request  , 'placement_partners.html' , context)



def create_trees(request):
    context = {'isa_id_list' : isa_id_list}

    return render(request, 'create_trees.html' , context)

def create_watershed_data(request):
    context = {'isa_id_list' : isa_id_list}

    return render(request , 'creater_water.html' , context)


def scheduled_interviews(request):
    context = {'datas' : ScheduleInterview.objects.all()}
    return render(request , 'scheduled_interviews.html' , context)


def manage_trees_data(request):
    current_year = 2021
    context = {
        'trees_objs' : TreePlantation.objects.all(),
        'current_year' : TreePlantation.objects.filter(date_of_plantation__icontains= str(current_year)).count(),
        'previous_year' : TreePlantation.objects.filter(date_of_plantation__icontains= str(current_year-1)).count(),
        'total' : TreePlantation.objects.count()
        }

    
    

    return render(request , 'manage_trees.html' , context)

def manage_watershed_data(request):
    context = {'water_objs' : WatershedData.objects.all()}
    return render(request , 'manage_water.html' , context)



def view_tree_plantation_images(request , id):
    context = {}
    try:
        tree_plantation = TreePlantation.objects.get(id = id)
        images = TreePlantationPhotos.objects.filter(tree_plantation=tree_plantation)
        context['images'] = images
        context['tree'] = tree_plantation

    except Exception as e:
        print(e)

    return render(request , 'view_tree_images.html' , context)




def view_water_shed_images(request , id):
    context = {}
    try:
        water_shed_data = WatershedData.objects.get(id = id)
        images = WatershedDataPhotos.objects.filter(water_shed_data=water_shed_data)
        context['images'] = images
        context['water_shed_data'] = water_shed_data

    except Exception as e:
        print(e)
    print(context)
    return render(request , 'view_water_shed_images.html' , context)



def payments(request):
    context = {'payment_objs' : PaymentSheet.objects.all()}
    return render(request , 'payments.html' , context)



def upload_payments(request):
    context = {'upload_payment_objs' : PaymentUpload.objects.all()}
    return render(request , 'upload_payments.html' , context)





def search_payments(request):
    context = {}
    if request.GET.get('emp_id'):
        context = {'payment_objs' : PaymentSheet.objects.filter(Employee_Code = request.GET.get('emp_id'))}
        print(context)
    return render(request , 'search_payments.html' , context)


from console.utils_api import search_trainee

def filter_data(request):
    context = {}

    if request.GET.get('name') and  request.GET.get('phone_no'):
        name = request.GET.get('name')
        phone_no = request.GET.get('phone_no')
        data = search_trainee(name , phone_no)

        context = {'datas' : data['details']}

    return render(request , 'filter_data.html' , context)



def view_issue_ceritficate(request):
    context = {}
    certificates  = Certificate.objects.all()
    if request.GET.get('trainee_id'):
        certificates = certificates.filter(trainee_id__trainee_id = request.GET.get('trainee_id'))

    context['certificates'] = certificates
    return render(request , 'view_issue_ceritficate.html' , context)








def create_certificate_templates(request):
    return render(request , 'certificate/create_certificates.html')

def show_certificate_template(request , id):
    try:
        context = {'cerificate_obj' : CertificateTemplates.objects.get(id = id)}
        return render (request , 'certificate/show_certificate.html' , context)
    except Exception as e:
        print(e)

def update_certificate_template(request , id):
    try:
        context = {'cerificate_obj' : CertificateTemplates.objects.get(id = id)}
        return render (request , 'certificate/update_certificate.html' , context)
    except Exception as e:
        print(e)

def manage_certificate_templates(request):
    context = {'ceritificates' : CertificateTemplates.objects.all()}
    return render(request , 'certificate/manage_certificates.html' , context)


def add_organization(request):
    context = {'isa_id_list' : isa_id_list}
    return render(request , 'financial/add_organization.html' , context)


def manage_organization(request):
    context = {'financial_organizations' : FinancialOrganization.objects.filter(to_show =True)}

    return render(request , 'financial/manage_organization.html' , context)

def add_session(request):
    context = {'isa_id_list' : isa_id_list , 'financial_organizations' : FinancialOrganization.objects.all()}
    print(context)
    return render(request , 'financial/add_sessions.html' , context)


def manage_session(request):
    context = {'financial_sessions' : FinancialSession.objects.all()}

    return render(request , 'financial/manage_sessions.html' , context)


def impact_upload(request):
    context = {'impact_uploads' : ImpactBoxUpload.objects.all()}
    return render(request , 'uploads/impact_upload.html' , context)

def delete_uploaded_impact(request , id):
    try:
        obj = ImpactBoxUpload.objects.get(id = id)
        obj.delete()
    except Exception as e:
        print(e)

    return redirect('/reports/impact-upload/')




from console.utils_api import *


def view_gal(request):
    context = {}
    try:
        search_query = None
        flag = -1
        if request.GET.get('search_query'):
            search_query = request.GET.get('search_query')

            if len(search_query) > 1 and search_query[1].isdigit():
                flag = 0
            else :
                flag = 1

        context['gal_datas'] = get_gal_data(search_query , flag)
    except Exception as e:
        print(e)
    
    return render(request , 'gal/view_gal.html' , context)


def view_detailed_gal(request , emp_id):
    context = {}

    return render(request , 'gal/view_detailed_gal.html' , context)


def show_hrms(request):
    context = {'job_postings' : InternalJobPosting.objects.filter(is_active=True) , 'policies_objs' : Policies.objects.all()}
    return render(request , 'hrms/show_hrms.html' , context)


def upload_internal_job_postings(request):
    context = {'form' : JobForm, 'job_postings' : InternalJobPosting.objects.all()}
    
  
    try:
        if request.method == 'POST':
            form = JobForm(request.POST)
            job_position = request.POST.get('job_position')
            job_location = request.POST.get('job_location')
        
            if form.is_valid():
                job_description = form.cleaned_data['job_description']
                InternalJobPosting.objects.create(
                        position = job_position,
                        location = job_location,
                        job_description = job_description,
                    )
                return redirect('/reports/upload-internal-job-postings/')
    except Exception as e:
            print(e)
    
    return render(request , 'jobposting/upload_inter_job_postings.html' , context)


from .forms import *

def upload_job_posting(request , id):
    context = {}

    try:
        if request.method == 'POST':
            form = JobForm(request.POST)
            job_position = request.POST.get('job_position')
            job_location = request.POST.get('job_location')
            try:
                if form.is_valid():
                    job_description = form.cleaned_data['job_description']
                    internal_job_obj = InternalJobPosting.objects.get(id = id)
                    internal_job_obj.job_position = job_position
                    internal_job_obj.job_location = job_location
                    internal_job_obj.job_description = job_description
                    internal_job_obj.save()

                    return redirect(f'/reports/update-job-posting/{id}/')
            except Exception as e:
                print(e)
        
        job_obj = InternalJobPosting.objects.get(id = id)
        initial_dict = {'job_description' : job_obj.job_description}
        form = JobForm(initial=initial_dict)
      
        context = {'form' : form, 'job_posting_obj' : InternalJobPosting.objects.get(id = id)}

                
    except Exception as e:
        print(e)


    
    
    print(context)
    return render(request , 'jobposting/update_job_posting.html'  , context)




def delete_job_posting(request, id):
    try:
        job_posting_obj =  InternalJobPosting.objects.get(id = id)
        job_posting_obj.delete()
    
    except Exception as e:
        print(e)

    return redirect('/reports/upload-internal-job-postings/')


def view_policy(request , id):
    context = {}
    try:
        policy_obj = Policies.objects.get(id = id)
        context['policy_obj'] = policy_obj
    except Exception as e:
        print(e)
    
    return render(request , 'policy/view_policy.html' , context)

