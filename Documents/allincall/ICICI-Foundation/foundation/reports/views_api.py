from reports.views import payments
from django.core.checks.messages import Info
from django.db import reset_queries
from django.http import response
from django.shortcuts import redirect, render
from .models import *
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
from  console.utils_api import get_upcoming_batch_list , get_batch_data , get_batch_details ,get_custom_enrolled_trainee
from accounts.models import *
from console.models import *
from django.http import HttpResponseForbidden
from accounts.auth import *
from django.utils.dateparse import parse_date
import datetime
import os
from .helpers import *
from console.constants import isa_id_list
from home.models import *


logging.basicConfig()
logger = logging.getLogger(__name__)

from rest_framework import permissions


BASE_DIR = settings.BASE_DIR




class AssignFollowups(APIView):
    
    
    def post(self, request):
        response = {}
        response['status_code'] = 500
        response['message'] = 'Something went wrong'
        try:
            data = request.data
        
            pk_lists = data.get('pk_lists')
            follow_up_title = data.get('follow_up_title')
            follow_up_deadline = data.get('follow_up_deadline')
            
            if is_html(follow_up_title):
                response['message'] = 'Not a valid text'
                raise Exception('Not a valid text')
                
                
            
            
            for pk_list in pk_lists:
                batch_follow_ups_obj = BatchFollowups.objects.filter(trainee_id = pk_list['trainee_id']).first()
                try:
                    if batch_follow_ups_obj is None:
                        # datetime.datetime.strptime(pk_list['batch_start_date'], "%Y-%m-%d").date()
                        #batch_start_date  =  datetime.datetime.strptime(pk_list['batch_start_date'], "%m-%d-%Y").date()

                       # batch_end_date = datetime.datetime.strptime(pk_list['batch_end_date'], "%m-%d-%Y").date()

                        
                        BatchFollowups.objects.create(
                            trainee_id = pk_list['trainee_id'],
                        trainee_name = pk_list['trainee_name'],
                        batch_id = pk_list['batch_id'],
                        batch_start_date =pk_list['batch_start_date'],
                        batch_end_date = pk_list['batch_end_date'],
                        application_id = pk_list['applicant_id']
                        )
                except Exception as e:
                    print(e)
                    
            
            assign_to_user_obj = Profile.objects.filter(id = data.get('assign_to_user')).first()
            follow_up_deadline = datetime.datetime.strptime(follow_up_deadline, "%Y-%m-%d").date()
            user_batch_followups_obj = UserBatchFollowups.objects.create(
                assign_to_user =assign_to_user_obj,
                title = follow_up_title , 
                assigned_by_user=request.user,
                completion_date_for_followups = follow_up_deadline
                )
            
            for pk_list in pk_lists:
                batch_follow_ups_obj = BatchFollowups.objects.filter(trainee_id = pk_list['trainee_id']).first()
                user_batch_followups_obj.batch_followups.add(batch_follow_ups_obj)
                batch_follow_ups_obj.save()
                
            #BatchFollowUpsRecord.objects.create(assigned_to_user=assign_to_user_obj , assigned_by_user=request.user  ,  count_of_followups =len(pk_lists) )
            
            
            response['status_code'] = 200
            response['message'] = 'Followups created'

        except Exception as e:
            print(e)
            
        return Response(response)                
            
AssignFollowups= AssignFollowups.as_view()






''' TRIGGER IS A GET API WHICH TAKES TWO QUERY STRING ID AND A OPTION AND CALLS THE APPROPRIATE FUNCTION '''

class  Trigger(APIView):

    def get(self  , request):
        response = {}
        response['status_code'] = 500
        try:
            id = request.GET.get('id')
            option = request.GET.get('option')


            if id is None or option is None:
                response['status_code'] = 401
                response['message'] =  'both id and options are required'
                raise Exception('both id and options are required')
            try:
                staus = False
                if int(option)  == 1:
                    source_report = SourcingReportStatus.objects.get(id = id)
                    source_report.triggered_status = True
                    source_report.current_status =  2

                    source_report.save()
                    status = import_source_from_excel(source_report.file_path ,source_report.user  , source_report)
                elif int(option)  == 2:
                    follow_up_report = FollowUpsReportStatus.objects.get(id=id)
                   
                    status = import_follow_ups_from_excel(follow_up_report.file_path , follow_up_report.user , follow_up_report )
                    if status:
                        follow_up_report.triggered_status = True
                        follow_up_report.current_status =  2
                        follow_up_report.save()
                        
                elif int(option) == 3:
                    print(id)
                    enrollment_report = EnrollmentReportStatus.objects.get(id = id)
                    enrollment_report.current_status =  2
                    enrollment_report.triggered_status = True
                    enrollment_report.save()
                 
                    status = import_enrollments_from_excel(enrollment_report.file_path ,enrollment_report.user  , enrollment_report)
                else:
                    response['message'] =  'Wrong option'
                    raise Exception('Wrong option')

                if status:
                    response['status_code'] = 200
                    response['message'] =  'Successfully imported'

            except Exception as e:
                print(e)
                exc_type, exc_obj, exc_tb = sys.exc_info()
                logger.error(f"Trigger {str(e)} at {str(exc_tb.tb_lineno)}")
                response['status_code'] = 401
                response['message'] =  'Invalid Id'
                raise Exception('Invalid Id')


        except Exception as e:
            print(e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error(f"Trigger {str(e)} at {str(exc_tb.tb_lineno)}")
            response['status_code'] = 401
            response['message'] =  'Something went wrong'

        return Response(data =response)

    
Trigger = Trigger.as_view()



class  SendSMS(APIView):

    def get(self  , request):
        response = {}
        response['status_code'] = 500
        try:
            id = request.GET.get('id')
            option = request.GET.get('option')


            if id is None or option is None:
                response['status_code'] = 401
                response['message'] =  'id and option both are required'
                raise Exception('id and option both are required')

            try:
                if int(option) == 1:
                    source_report = SourcingReportStatus.objects.get(id = id)
                    source_report.current_status = 4
                    source_report.triggered_status = True
                    source_report.save()
                    send_sms_and_email_sourcing(source_report ,request.user)
                elif int(option) == 2:
                    follow_up_report = FollowUpsReportStatus.objects.get(id=id)
                    follow_up_report.current_status = 4
                    follow_up_report.triggered_status = True
                    follow_up_report.save()
                    print(follow_up_report)
                    send_sms_and_email_follow(follow_up_report, request.user)
                elif int(option) == 3:
                    enrollment_report = EnrollmentReportStatus.objects.get(id=id)
                    enrollment_report.current_status = 4
                    enrollment_report.triggered_status = True
                    enrollment_report.save()
                    print(enrollment_report)
                    send_sms_and_email_enrollment(enrollment_report, request.user)
                else:
                    response['status_code'] = 401
                    response['message'] =  'invalid option'
                    raise Exception('Invaild option')

                response['status_code'] = 200
                response['message'] =  'Messages sent successfully'


            except Exception as e:
                print(e)
                exc_type, exc_obj, exc_tb = sys.exc_info()
                logger.error(f"SendSMS {str(e)} at {str(exc_tb.tb_lineno)}")
                print(f"SendSMS {str(e)} at {str(exc_tb.tb_lineno)}")
                response['status_code'] = 401
                response['message'] =  'Invalid Id'
                raise Exception('Invalid Id')

            

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error(f"SendSMS {str(e)} at {str(exc_tb.tb_lineno)}")
            print(f"SendSMS {str(e)} at {str(exc_tb.tb_lineno)}")

            response['status_code'] = 401
            response['message'] =  'Something went wrong'

        return Response(data =response)

SendSMS = SendSMS.as_view()




class FetchApplicants(APIView):

    def get(self  , request):
        response = {}
        response['status_code'] = 500
        try:
            id = request.GET.get('id')
            option = request.GET.get('option')
            if id is None or option is None:
                response['status_code'] = 401
                response['message'] =  'both option and id are required'
                raise Exception('both option and id are required')
            try:
                if int(option) == 1:
                    source_report = SourcingReportStatus.objects.get(id = id)
                    source_report.current_status = 3
                    source_report.save()
                    response['status_code'] = 200
                    response['message'] =  'Refreshed Applicants'
                    fetch_applicant_id(source_report ,request.user)
                elif int(option) == 2:
                    follow_up_report = FollowUpsReportStatus.objects.get(id=id)
                    follow_up_report.current_status = 3
                    follow_up_report.save()
                    response['status_code'] = 200
                    response['message'] =  'Refreshed Follow Ups'
                    fetch_follow_up_data(follow_up_report , request.user)
                elif int(option) == 3:
                    enrollment_report = EnrollmentReportStatus.objects.get(id = id)
                    enrollment_report.triggered_status = True
                    enrollment_report.current_status = 3

                    enrollment_report.save()
                    response['status_code'] = 200
                    response['message'] =  'Refreshed Enrollments'
                    fetch_enrollment_data(enrollment_report  , request.user)
                else:
                    response['message'] =  'Wrong option'
                    raise Exception('Wrong option')



            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                logger.error(f"FetchApplicants {str(e)} at {str(exc_tb.tb_lineno)}")
                response['error'] = str(e)
                response['status_code'] = 401
                response['message'] =  'Invalid Id'
                raise Exception('Invalid Id')


        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error(f"FetchApplicants {str(e)} at {str(exc_tb.tb_lineno)}")
            response['error'] = str(e)
            response['status_code'] = 401
            response['message'] =  'Something went wrong'

        return Response(data =response)

FetchApplicants = FetchApplicants.as_view()







class ImportSourcing(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self , request):
        response = {}
        response['status_code'] = 500
        response['message'] = 'Something went wrong'
        response['errors'] = []
        errors = []
        excel_data = []
        try:
            # if not request.user.superuser_status:
            #     response['status_code'] = 500
            #     response['message'] = 'Invalid Access'
            #     raise Exception("Invalid Access")
                
            uploaded_file = request.FILES.get('excel_file')
            if uploaded_file is None:
                response['status_code'] = 301
                response['errors'] = errors
                response['message'] = 'File is required'
                raise Exception('File is required')


            file_extension = str(uploaded_file).split('.')[-1].lower()
            errors , status  = None , None
            if (file_extension not in ["xlx", "xlsx"]):
                logger.info("File Extension not allowed file=%s",
                                str(uploaded_file))
                response["status"] = 301 
            else:
                
                try:
                    file_path = saveFile(uploaded_file)

                    correct_path = str(BASE_DIR) + '/public/static/' +file_path
                    logger.info("File Saved %s", str(correct_path))
                    errors , status =  check_source_from_excel(correct_path , request.user)

                except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    logger.error(f"ImportSourcing {str(e)} at {str(exc_tb.tb_lineno)}")

    
            if status:
                response['status_code'] = 200
                response['errors'] = errors
                response['message'] = 'File uploaded successfully'
            else:
                response['status_code'] = 300
                response['errors'] = json.loads(errors)
                response['message'] = 'Excel has errors please review'
                
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error(f"ImportSourcing {str(e)} at {str(exc_tb.tb_lineno)}")

        return Response(data=response)
    

ImportSourcing = ImportSourcing.as_view()



import json
class GetErrors(APIView):

    def get(self , request):
        response = {}
        response['status_code'] = 500
        response['errors'] = []
        try:
            id = request.GET.get('id')
            option = request.GET.get('option')

            if id is None or option is None:
                response['status_code'] = 401
                response['message'] =  'both id and option are required'
                raise Exception('both id and option are required')

            try:
                if int(option) == 1:
                    source_report = SourcingReportStatus.objects.get(id = id)
                    errors = (source_report.errors_desc)
                    response['errors'] = json.loads(errors)

                elif int(option) == 2:
                    follow_up_report = FollowUpsReportStatus.objects.get(id =id)
                    errors = (follow_up_report.errors_desc)
                    response['errors'] = json.loads(errors)
                elif int(option) == 3:
                    enrollment_report = EnrollmentReportStatus.objects.get(id=id)
                    print(enrollment_report)
                    errors = (enrollment_report.errors_desc)
                    response['errors'] = json.loads(errors)
                else:
                    response['message'] = 'invalid option'
                    raise Exception ('invalid option')
                    
                response['message'] = 'All errors'
            except Exception as e:
                print(e)
                response['message'] =  'invalid id'
                response['status_code'] = 200
            


        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error(f"GetErrors {str(e)} at {str(exc_tb.tb_lineno)}")
            print(e)
            response['errors'] = []
            response['status_code'] = 401
            response['message'] =  'Something went wrong'

        return Response(data =response)


GetErrors  = GetErrors.as_view()



''' REMOVE IS GET A GET API WHICH TAKES TWO QUERY STRING ID AND A OPTION AND TOGGLE THE VISIBILITY OF APPROPRIATE MODEL INSTANCE '''

class Remove(APIView):
    def get(self , request):
        response = {}
        response['status_code'] = 500
        try:
            id = request.GET.get('id')
            option = request.GET.get('option')
            if id is None or option is None:
                response['status_code'] = 401
                response['message'] =  'both id and option are required'
                raise Exception('both id and option are required')
            try:
                if int(option) == 1:
                    source_report = SourcingReportStatus.objects.get(id = id)
                    if source_report.is_visible:
                        response['message'] =  'Visibility set to off'
                    else:
                        response['message'] =  'Visibility set to on'
                    source_report.is_visible = not  source_report.is_visible
                    source_report.save()
                elif int(option) == 2:
                    follow_up_report = FollowUpsReportStatus.objects.get(id =id)
                    if follow_up_report.is_visible:
                        response['message'] =  'Visibility set to off'
                    else:
                        response['message'] =  'Visibility set to on'
                    follow_up_report.is_visible = not  follow_up_report.is_visible
                    follow_up_report.save()
                elif int(option) == 3:
                    enrollment_report = EnrollmentReportStatus.objects.get(id=id)
                    if enrollment_report.is_visible:
                        response['message'] =  'Visibility set to off'
                    else:
                        response['message'] =  'Visibility set to on'
                    enrollment_report.is_visible = not  enrollment_report.is_visible
                    enrollment_report.save()
                else:
                    response['message'] = 'invalid option'
                    raise Exception ('invalid option')
            
                response['status_code'] = 200

            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                logger.error(f"GetErrors {str(e)} at {str(exc_tb.tb_lineno)}")
                response['status_code'] = 401
                response['message'] =  'Invalid Id'
                raise Exception('Invalid Id')


        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error(f"GetErrors {str(e)} at {str(exc_tb.tb_lineno)}")
            response['status_code'] = 401
            response['message'] =  'Something went wrong'

        return Response(data =response)


Remove = Remove.as_view()





class ImportFollowUps(APIView):
    def post(self , request):
        response = {}
        response['status_code'] = 500
        response['message'] = 'Something went wrong'
        response['errors'] = []
        errors = []
        excel_data = []
        try:
            # if not request.user.superuser_status:
            #     response['status_code'] = 500
            #     response['message'] = 'Invalid Access'
            #     raise Exception("Invalid Access")
                
            uploaded_file = request.FILES.get('excel_file')
            if uploaded_file is None:
                response['status_code'] = 301
                response['errors'] = errors
                response['message'] = 'File is required'
                raise Exception('File is required')


            file_extension = str(uploaded_file).split('.')[-1].lower()
            errors , status  = None , None
            if (file_extension not in ["xlx", "xlsx"]):
                logger.info("File Extension not allowed file=%s",
                                str(uploaded_file))
                response["status"] = 301 
            else:
                
                try:
                    file_path = saveFile(uploaded_file)

                    correct_path = str(BASE_DIR) + '/public/static/' +file_path
                    logger.info("File Saved %s", str(correct_path))
                    errors , status =  check_follow_ups_from_excel(correct_path , request.user)

                except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    logger.error(f"ImportSourcing {str(e)} at {str(exc_tb.tb_lineno)}")

    
            if status:
                response['status_code'] = 200
                response['errors'] = errors
                response['message'] = 'File uploaded successfully'
            else:
                response['status_code'] = 300
                response['errors'] = json.loads(errors)
                response['message'] = 'Excel has errors please review'
                
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error(f"ImportFollowUps {str(e)} at {str(exc_tb.tb_lineno)}")

        return Response(data=response)

ImportFollowUps = ImportFollowUps.as_view()
class  TriggerFolowUps(APIView):

    def get(self  , request):
        response = {}
        response['status_code'] = 500
        try:
            id = request.GET.get('id')
            if id is None:
                response['status_code'] = 401
                response['message'] =  'Invalid Id'
                raise Exception('Invalid Id')
            try:
                follow_up_report = FollowUpsReportStatus.objects.get(id = id)
                follow_up_report.triggered_status = True
                follow_up_report.save()
                response['status_code'] = 200
                response['message'] =  'Follow ups triggered Successfully'
                import_follow_ups_from_excel(follow_up_report.file_path ,follow_up_report.user  , follow_up_report)
            except Exception as e:
                response['status_code'] = 401
                response['message'] =  'Invalid Id'
                raise Exception('Invalid Id')


        except Exception as e:
            print(e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error(f"GetBatchDetails {str(e)} at {str(exc_tb.tb_lineno)}")
            response['status_code'] = 401
            response['message'] =  'Something went wrong'

        return Response(data =response)

    
TriggerFolowUps = TriggerFolowUps.as_view()





class ImportEnrollments(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self , request):
        response = {}
        response['status_code'] = 500
        response['message'] = 'Something went wrong'
        response['errors'] = []
        errors = []
        excel_data = []
        try:
            # if not request.user.superuser_status:
            #     response['status_code'] = 500
            #     response['message'] = 'Invalid Access'
            #     raise Exception("Invalid Access")
                
            uploaded_file = request.FILES.get('excel_file')
            if uploaded_file is None:
                response['status_code'] = 301
                response['errors'] = errors
                response['message'] = 'File is required'
                raise Exception('File is required')


            file_extension = str(uploaded_file).split('.')[-1].lower()
            errors , status  = None , None
            if (file_extension not in ["xlx", "xlsx"]):
                logger.info("File Extension not allowed file=%s",
                                str(uploaded_file))
                response["status"] = 301 
            else:
                
                try:
                    file_path = saveFile(uploaded_file)

                    correct_path = str(BASE_DIR) + '/public/static/' +file_path
                    logger.info("File Saved %s", str(correct_path))
                    errors , status =  check_enrollment_from_excel(correct_path , request.user)

                except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    logger.error(f"ImportSourcing {str(e)} at {str(exc_tb.tb_lineno)}")

    
            if status:
                response['status_code'] = 200
                response['errors'] = errors
                response['message'] = 'File uploaded successfully'
            else:
                response['status_code'] = 300
                response['errors'] = json.loads(errors)
                response['message'] = 'Excel has errors please review'
                
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error(f"ImportSourcing {str(e)} at {str(exc_tb.tb_lineno)}")

        return Response(data=response)
    

ImportEnrollments = ImportEnrollments.as_view()



class TriggerEnrollments(APIView):
    def get(self  , request):
        response = {}
        response['status_code'] = 500
        try:
            id = request.GET.get('id')
            if id is None:
                response['status_code'] = 401
                response['message'] =  'id is required'
                raise Exception('id is required')
            try:
                enrollment_report = EnrollmentReportStatus.objects.get(id = id)
                enrollment_report.triggered_status = True
                enrollment_report.save()
                response['status_code'] = 200
                response['message'] =  'Follow ups triggered Successfully'
                import_enrollments_from_excel(enrollment_report.file_path ,enrollment_report.user  , enrollment_report)
            except Exception as e:
                response['status_code'] = 401
                response['message'] =  'Invalid Id'
                raise Exception('Invalid Id')


        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error(f"GetBatchDetails {str(e)} at {str(exc_tb.tb_lineno)}")
            response['status_code'] = 401
            response['message'] =  'Something went wrong'

        return Response(data =response)


TriggerEnrollments = TriggerEnrollments.as_view()



class SendSMStoSpecificUser(APIView):
    def post(self , request):
        response = {}
        response['status_code'] = 500
        response['message'] = 'Something went wrong'
        try:
            data = request.data
            print(data)
            option = data.get('option')
            selected_option = data.get('selected_option' , 1)

            if selected_option is None:
                selected_option = 1
            print(selected_option)

            if option is None:
                response['status_code'] = 401
                response['message'] = 'option is required'      
                raise Exception('option is required')          


            pk_lists = data.get('pk_lists')

            if pk_lists is None:
                response['status_code'] = 401
                response['message'] = 'pk lists is required'
                raise Exception('Pk list is required')

            pk_lists =list(map(int , pk_lists))

            result = False
            objs = []
            option = int(option)
            if option == 1:
                objs = Enrollments.objects.filter(id__in = pk_lists) 
            elif option == 2:
                objs = Sourcing.objects.filter(id__in = pk_lists) 
            elif option == 3:
                objs = FollowUps.objects.filter(id__in = pk_lists)
            else:
                response['message'] = 'You have entered a wrong option'
                raise Exception('wrong option')
                
            selected_option = int(selected_option)

            
            if selected_option == 1:
                result = send_sms_and_email_to_objs(objs)
                if result:
                    response['message'] = 'sms sent'
            else:
                result = refresh_objs(objs , option)
                if result:
                    response['message'] = 'data refreshed'

            
            if result:
                response['status_code'] = 200
           


        except Exception as e:
            print(e)

        return Response(data = response)

SendSMStoSpecificUser = SendSMStoSpecificUser.as_view()



class FetchApplicantIdData(APIView):

    def get(self , request):
        response = {}
        response['status_code'] = 500
        response['message'] = 'Something went wrong'

        try:
            id = request.GET.get('id')
            
            if id is None:
                response['message'] = 'Id is required'
                raise Exception ('Id is required')
                
            sourcing_obj = Sourcing.objects.get(id =id)

            data = json.loads(sourcing_obj.application_id)

            response['data'] = data
            response['status_code'] = 200
            response['message'] = 'Data'
        except Exception as e:
            print(e)
        
        return Response(data = response)


FetchApplicantIdData = FetchApplicantIdData.as_view()




class GetBatchDetails(APIView):
    def get(self, request):
        response = {}
        response['status_code'] = 500
        response['message'] = 'Something went wrong'
        try:
            emp_id = request.GET.get('emp_id')
            if emp_id is None:
                raise Exception('Emp id is required')
            
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
            response['data'] = payload
            
        except Exception as e: 
            print(e)
    
        return Response(response)

GetBatchDetails = GetBatchDetails.as_view()


class IssueTraineeCeritficate(APIView):
    def post(self , request):
        response = {}
        response['status_code'] = 500
        response['message'] = 'Something went wrong'
        try:
            data = request.data

            data = json.loads(data.get('data'))

            pk_lists = data.get('pk_lists')
            template_id = data.get('template_id')
            custom_course = data.get('custom_course')
            isa_id   = data.get('isa_id')
            start_date   = data.get('start_date')
            end_date   = data.get('end_date')
            
            trainee_objs = []
    
            for pk_list in pk_lists:
                trainee_obj = Trainee.objects.filter(trainee_id=pk_list['trainee_id']).first()
                
                trainee_objs.append(trainee_obj)

            
            
                
                if trainee_obj:
                    trainee_obj.is_certificate_issued = True
                    trainee_obj.save()  

            #IssueCertificateThread(trainee_objs).run()
            #AddBatchesTodb(pk_lists , batch_room_code).run()

            save_pdf(trainee_objs , template_id , custom_course , isa_id,start_date, end_date)

            response['status_code'] = 200
            response['message'] = 'Ceritificate issue process started'
            
        except Exception as e: 
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error(f"GetErrors {str(e)} at {str(exc_tb.tb_lineno)}") 
        return Response(response)
    
IssueTraineeCeritficate= IssueTraineeCeritficate.as_view()
    

class StoreTraineeList(APIView):
    def post(self , request):
        response = {}
        response['status_code'] = 500
        response['message'] = 'Something went wrong'
        try:
            data = request.data
            pk_lists = json.loads(data.get('data'))
            
            for pk_list in pk_lists:
                print(pk_list)
                if Trainee.objects.filter(trainee_id=pk_list['trainee_id']).first() is None:
                    Trainee.objects.create(trainee_id = pk_list['trainee_id'],
                                        applicant_id = pk_list['applicant_id'],
                                        trainee_name = pk_list['trainee_name'],
                                        batch_id = pk_list['batch_id'],
                                        
                                        )
                    
            
            response['status_code'] = 200
            response['message'] = 'Trainee imported successfully'
            
        except Exception as e: 
            print(e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error(f"GetErrors {str(e)} at {str(exc_tb.tb_lineno)}") 
    
        return Response(response)
    
StoreTraineeList = StoreTraineeList.as_view()


class StoreBatchList(APIView):
    def post(self , request):
        response = {}
        response['status_code'] = 500
        response['message'] = 'Something went wrong'
        try:
            data = request.data
            pk_lists = json.loads(data.get('data'))
            

            batch_room_code = random_sting(5)
            IncrementBatchCounter.objects.create(socket_id=batch_room_code , end_count=len(pk_lists))
            store_batch_to_db(pk_lists , batch_room_code)
            print(batch_room_code)
            #AddBatchesTodb(pk_lists , batch_room_code).run()
            
            
            
            # for pk_list in pk_lists:
            #     if Batch.objects.filter(batch_id=pk_list['batch']).first() is None:
            #         Batch.objects.create(batch_id = pk_list['batch'],
            #                             emp_id = pk_list['emp_id'],
            #                             batch_start = pk_list['batch_start_date']
            #                             )
                    
            
            response['status_code'] = 200
            response['message'] = 'Batch created successfully'
            response['batch_room_code'] = batch_room_code
            
        except Exception as e: 
            print(e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error(f"GetErrors {str(e)} at {str(exc_tb.tb_lineno)}") 
    
        return Response(response)

StoreBatchList = StoreBatchList.as_view()








class UploadUsers(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self , request):
        response = {}
        response['status_code'] = 500
        response['message'] = 'Something went wrong'
        response['errors'] = []
        errors = []
        excel_data = []
        try:
            # if not request.user.superuser_status:
            #     response['status_code'] = 500
            #     response['message'] = 'Invalid Access'
            #     raise Exception("Invalid Access")
                
            uploaded_file = request.FILES.get('excel_file')
            # print('arrived')
            # FileUpload.objects.create(file =uploaded_file )
            
            #return Response({'status_code' : 200, 'message' : 'uploaded'})
            
            if uploaded_file is None:
                response['status_code'] = 301
                response['errors'] = errors
                response['message'] = 'File is required'
                raise Exception('File is required')


            file_extension = str(uploaded_file).split('.')[-1].lower()
            errors , status  = [] , None
            if (file_extension not in ["xlx", "xlsx"]):
                logger.info("File Extension not allowed file=%s",
                                str(uploaded_file))
                response["status"] = 301 
            else:
                
                try:
                    file_path = saveFile(uploaded_file)

                    correct_path = str(BASE_DIR) + '/public/static/' +file_path
                    logger.info("File Saved %s", str(correct_path))
                    errors , status =  check_users_from_excel(correct_path ,  file_path)

                except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    logger.error(f"ImportSourcing {str(e)} at {str(exc_tb.tb_lineno)}")

    
            if status:
                response['status_code'] = 200
                response['errors'] = errors
                response['message'] = 'File uploaded successfully'
            else:
                response['status_code'] = 300
                print(errors)
                if not isinstance(errors, list):
                    response['errors'] = json.loads(errors)
                response['message'] = 'Excel has errors please review'
                
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error(f"ImportSourcing {str(e)} at {str(exc_tb.tb_lineno)}")

        return Response(data=response)
    

UploadUsers = UploadUsers.as_view()



class DownloadUsers(APIView):
    
    def get(self,request):
        response = {}
        response['status_code'] = 500
        response['message'] = 'Something went wrong'
        try:
            user_objs = Profile.objects.all()
            link , status = export_users_excel(user_objs)
            
            if not status:
                raise Exception('Something went wrong')
            response['link'] = link
            response['status_code'] = 200
            response['message'] = 'Your file'
            
        except Exception as e:
            print(e) 
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error(f"GetErrors {str(e)} at {str(exc_tb.tb_lineno)}")    
        return Response(response)


DownloadUsers = DownloadUsers.as_view()



class ImportUsers(APIView):
    def get(self , request):
        response = {}
        response['status_code'] = 500
        response['message'] = 'Something went wrong'
        try:
            id = request.GET.get('id')

            if id:
                upload_obj = UserUploadExcel.objects.get(id = id)
                upload_obj.is_imported = True
                upload_obj.save()
                status = import_users( str(BASE_DIR) + '/public/static/' + upload_obj.file_path)

                if status:
                    response['status_code'] = 200
                    response['message'] = 'File Imported'
        except Exception as e :
            print(e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error(f"GetErrors {str(e)} at {str(exc_tb.tb_lineno)}") 
        
        return Response(response)


ImportUsers = ImportUsers.as_view()






class GetUserErrors(APIView):
    def get(self , request): 
        response = {}
        response['status_code'] = 500
        response['errors'] = []
        response['message'] = 'Something went wrong'
        try:
            id = request.GET.get('id')

            if id is None :
                response['status_code'] = 401
                response['message'] =  ' id is required'
                raise Exception('both id and option are required')
                
            user_upload_objs = UserUploadExcel.objects.get(id =id)
            response['errors'] = json.loads(user_upload_objs.errors_desc)
            response['status_code'] = 200
            response['message'] = 'All errors'

        
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error(f"GetErrors {str(e)} at {str(exc_tb.tb_lineno)}")
            print(e)
            response['errors'] = []
            response['status_code'] = 401
            response['message'] =  'Something went wrong'

        return Response(data =response)

GetUserErrors= GetUserErrors.as_view()



class GetRolesExcel(APIView):
    def get(self , request):
        response = {}
        response['status_code'] = 500
        response['message'] = 'Something went wrong'
        try:
            roles_obj = Role.objects.all()
            print(roles_obj)
            file_path , status = export_roles(roles_obj) 

            if status:
                response['link'] = file_path
                response['status_code'] = 200

        except Exception as e:
            print(e)   
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error(f"GetErrors {str(e)} at {str(exc_tb.tb_lineno)}")     
        return Response(response)

GetRolesExcel = GetRolesExcel.as_view()




class UploadFile(APIView):
    def post(self , request):
        response = {'status' : 200}
        try:
            data = request.data
        except Exception as e:
            print(e)
        
        return Response(response)

UpdateFile = UploadFile.as_view()
            

class CreateRefferal(APIView):
    def post(self , request):
        response = {}
        response['status_code'] = 500
        response['message'] = 'Something went wrong'
        try:
            print("Hello")
            data = request.data
            print(data)
            referrer_name     = data.get('referrer_name')
            referrer_mobile   = data.get('referrer_mobile')
            referrer_email = data.get('referrer_email')

            referee_name   = data.get('referee_name')
            referee_email   = data.get('referee_email')
            referee_mobile = data.get('referee_mobile')
            source   = data.get('source')


            print(data)

            if referrer_name is None:
                response['message'] = 'referrer_name is required'
                raise Exception('referrer_name is required')

            if referrer_mobile is None:
                response['message'] = 'referrer_mobile is required'
                raise Exception('referrer_mobile is required')

            if referee_name is None:
                response['message'] = 'referee_name is required'
                raise Exception('referee_name is required')

            if referee_email is None:
                response['message'] = 'referee_email is required'
                raise Exception('referee_email is required')

            if referee_email is None:
                response['message'] = 'source is required'
                raise Exception('source is required')


            Referral.objects.create(
                referrer_name   = referrer_name,
                referrer_mobile  = referrer_mobile,
                referrer_email  = referrer_email,

                referee_name  = referee_name,
                referee_mobile  = referee_mobile,
                referee_email  = referee_email,

                source  = source,
            )
            response['status_code'] = 200
            response['message'] = 'Referral created successfully'

        except Exception as e:
            #print(e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error(f"CreateRefferal {str(e)} at {str(exc_tb.tb_lineno)}")   
            print(f"CreateRefferal {str(e)} at {str(exc_tb.tb_lineno)}")   

        return Response(response)

CreateRefferal  = CreateRefferal.as_view()






class GetBacthListApi(APIView):
    def post(self , request):
        response = {}
        response['status_code'] = 500
        response['message'] = 'Something went wrong'

        try:
            data = request.data 

            
            isa_id = data.get('isa_id')
            course_id = data.get('course_id')
            batch_start_from_date = data.get('batch_start_from_date')
            batch_start_to_date = data.get('batch_start_to_date')

            payload = get_upcoming_batch_list(isa_id , course_id , batch_start_from_date ,  batch_start_to_date)

            response['status_code'] = 200
            response['message'] = 'all batches'
            response['data'] = payload['details']


            print(payload)
        except Exception as e:
            print(e)
        
        return Response(response)

GetBacthListApi= GetBacthListApi.as_view()



class CreatePayment(APIView):
    def get(self ,request):
        response = {}
        response['status_code'] = 500
        response['message'] = 'Something went wrong'
        try:
            id = request.GET.get('id')
            if id:
                payment_upload_obj = PaymentUpload.objects.get(id = id)
                payment_upload_obj.is_uploaded = True

                import_payment(payment_upload_obj.file_path)

                response['status_code'] = 500
                response['message'] = 'File is getting imported'

        except Exception as e:
            print(e)

        return Response(response)
            


    def post(self , request):
        response = {}
        response['status_code'] = 500
        response['message'] = 'Something went wrong'
        try:
             
            uploaded_file = request.FILES.get('excel_file')
            if uploaded_file is None:
                response['status_code'] = 301
                response['message'] = 'File is required'
                raise Exception('File is required')


            file_extension = str(uploaded_file).split('.')[-1].lower()
            errors , status  = None , None
            if (file_extension not in ["xlx", "xlsx"]):
                logger.info("File Extension not allowed file=%s",
                                str(uploaded_file))
                response["status"] = 301 
            else:
                
                try:
                    file_path = saveFile(uploaded_file)

                    correct_path = str(BASE_DIR) + '/public/static/' +file_path
                    logger.info("File Saved %s", str(correct_path))
                    print('@@@@@@@@@2')
                    print(file_path)
                    print(correct_path)
                    print('@@@@@@@@@2')

                    obj = PaymentUpload.objects.create(
                        file_path = correct_path
                    )
                    print(obj)
                    response['status_code'] = 200
                    response['message'] = 'File uploaded successfully'
                except Exception as e:
                    print(e)
        except Exception as e:
            print(e)
        
        return Response(response)


CreatePayment = CreatePayment.as_view()



class CreateOrganization(APIView):

    def get(self , request):
        response = {}
        response['status_code'] = 500
        response['message'] = 'Something went wrong'
        try:
            financial_organization = FinancialOrganization.objects.get(id = request.GET.get('id'))
            financial_organization.to_show = not financial_organization.to_show
            financial_organization.save()
            response['status_code'] = 200
            response['message'] = 'Success'

        except Exception as e:
            print(e)
        
        return Response(response)


    def post(self , request):
        response = {}
        response['status_code'] = 500
        response['message'] = 'Something went wrong'
        try:
            data = request.data
            name  = data.get('name')
            organization_type  = data.get('organization_type')
            address  = data.get('address')
            state  = data.get('state')
            district  = data.get('district')
            city  = data.get('city')
            pincode  = data.get('pincode')
            contact_person  = data.get('contact_person')
            designation  = data.get('designation')
            mobile  = data.get('mobile')
            email  = data.get('email')

            FinancialOrganization.objects.create(
                name  = name,
                organization_type  = organization_type,
                address  = address,
                state  = state,
                district  = district,
                city  = city,
                pincode  = pincode,
                contact_person  = contact_person,
                designation  = designation,
                mobile  = mobile,
                email  = email,
            )
            response['status_code'] = 200
            response['message'] = 'Financial organization created'

        except Exception as e:
            print(e)

        return Response(response)

CreateOrganization  = CreateOrganization.as_view()


class CreateFinancialOrganization(APIView):
    def post(self , request):
        response = {}
        response['status_code'] = 500
        response['message'] = 'Something went wrong'
        try:
            data = request.data
            uploaded_file = request.FILES.get('excel_file')
            if uploaded_file is None:
                response['status_code'] = 301
                response['message'] = 'File is required'
                raise Exception('File is required')

            program   = data.get('program')
            isa  = data.get('isa')
            state  = data.get('state')
            district  = data.get('district')
            village  = data.get('village')
            organization  = data.get('organization')
            mode  = data.get('mode')
            location  = data.get('location')
            topics_covered  = data.get('topics_covered')
            nature_of_participants  = data.get('nature_of_participants')
            start_time  = data.get('start_time')
            end_time  = data.get('end_time')
            no_of_events  = data.get('no_of_events')
            total_males  = data.get('total_males')
            total_females  = data.get('total_females')
            total_partipants  = data.get('total_partipants')

            images = request.FILES.getlist('images')

            start_time = convert_str_into_date(data.get('start_time'))
            end_time = convert_str_into_date(data.get('end_time'))

            if start_time is None:
                raise Exception('invalid start_date')
            
            if end_time is None:
                raise Exception('invalid end_time')

            
            financial_obj = FinancialSession.objects.create(
                counsellor_name = request.user.username,
                program  = program,
                isa  = isa,
                state  = state,
                district  = district,
                village  = village,
                
                mode  = mode,
                location  = location,
                topics_covered  = topics_covered,
                nature_of_participants  = nature_of_participants,
                start_time  = start_time,
                end_time  = end_time,
                no_of_events  = no_of_events,
                total_males  = total_males,
                total_females  = total_females,
                total_partipants  = total_partipants,
                excel = uploaded_file
            )
            try:
                if organization:
                    financial_organization_obj = FinancialOrganization.objects.get(id = organization)
                    financial_obj.organization = financial_organization_obj
                    financial_obj.save()
            except Exception as e:
                print(e)


                
            for image in images:
                try:
                    FinancialImages.objects.create(
                        financial_organization =financial_obj,
                        image = image
                    )
                except Exception as e:
                    print(e)
                
            response['status_code'] = 200
            response['message'] = 'Financial organization created'

        except Exception as e:
            print(e)

        return Response(response)


CreateFinancialOrganization  = CreateFinancialOrganization.as_view()




class CreateCertificate(APIView):

    def post(self , request):
        response = {}
        response['status_code'] = 500
        response['message'] = 'Something went wrong'
        try:
            data = request.data
            template_name = data.get('template_name')
            template_html = data.get('template_html')

            CertificateTemplates.objects.create(
                template_name=  template_name,
                content= template_html   
            )
            response['status_code'] = 200
            response['message'] = 'Ceritficate template created'

        except Exception as e:
            print(e)

        return Response(response)


CreateCertificate  = CreateCertificate.as_view()




class UploadImpactExcel(APIView):

    def get(self , request):
        response = {}
        response['status_code'] = 500
        response['message'] = 'Something went wrong'
        try:
            id = request.GET.get('id')

            if id:
                impact_upload_obj = ImpactBoxUpload.objects.get(id=id)
                import_impact_box(impact_upload_obj.file_path)
                impact_upload_obj.is_imported = True
                impact_upload_obj.save()

            response['status_code'] = 200
            response['message'] = 'Imported'
        except Exception as e:
            print(e)

        return Response(response)


    def post(self , request):
        response = {}
        response['status_code'] = 500
        response['message'] = 'Something went wrong'
        try:
            uploaded_file = request.FILES.get('excel_file')
            if uploaded_file is None:
                response['status_code'] = 301
                response['message'] = 'File is required'
                raise Exception('File is required')


            file_extension = str(uploaded_file).split('.')[-1].lower()
            errors , status  = None , None
            if (file_extension not in ["xlx", "xlsx"]):
                logger.info("File Extension not allowed file=%s",
                                str(uploaded_file))
                response["status"] = 301 
            else:
                
                try:
                    file_path = saveFile(uploaded_file)
                    correct_path = str(BASE_DIR) + '/public/static/' +file_path
                    logger.info("File Saved %s", str(correct_path))

                    #check_impact_box_upload(file_path)
                    ImpactBoxUpload.objects.create(
                     file_path = correct_path   
                    )

                    response['status_code'] = 200
                    response['message'] = 'File Imported Successfully'
                except Exception as e:
                    print(e)

        except Exception as e:
            print(e)


        return Response(response)


UploadImpactExcel= UploadImpactExcel.as_view()


class UploadInternalJobPosting(APIView):

    def get(self , request):
        response = {}
        response['status_code'] = 500
        response['message'] = 'Something went wrong'
        try:
            id = request.GET.get('id')
            if id:
                jobs_posting_obj = InternalJobPosting.objects.get(id = id)
                jobs_posting_obj.is_active = not jobs_posting_obj.is_active
                jobs_posting_obj.save()
                response['status_code'] = 200

        except Exception as e:
            print(e)

        return Response(response)


    def post(self , request):
        response = {}
        response['status_code'] = 500
        response['message'] = 'Something went wrong'
        try:
            uploaded_file = request.FILES.get('excel_file')
            print(uploaded_file)
            if uploaded_file is None:
                response['status_code'] = 301
                response['message'] = 'File is required'
                raise Exception('File is required')


            file_extension = str(uploaded_file).split('.')[-1].lower()
            errors , status  = None , None
            if (file_extension not in ["xlx", "xlsx"]):
                logger.info("File Extension not allowed file=%s",
                                str(uploaded_file))
                response["status"] = 301 
            else:
                
                try:
                    file_path = saveFile(uploaded_file)
                    correct_path = str(BASE_DIR) + '/public/static/' +file_path
                    logger.info("File Saved %s", str(correct_path))

                    import_internal_job_posting(correct_path)
                except Exception as e:
                    print(e)

                response['status_code'] = 200
                response['message'] = 'File uploaded'

        except Exception as e:
            print(e)  
        
        return Response(response)


UploadInternalJobPosting = UploadInternalJobPosting.as_view()


class CreateJobPosting(APIView):
    def post(self , request):
        response = {}
        response['status_code'] = 500
        response['message'] = 'Something went wrong'
        try:
            data = request.data
            print(data)
            job_position    = data.get('job_position')
            job_location    = data.get('job_location')
            job_description  = data.get('job_description')

            InternalJobPosting.objects.create(
                position   = job_position,
                location   = job_location,
                job_description   = job_description,
            )

            response['status_code'] = 200
            response['message'] = 'Job posting created'


        
        except Exception as e:
            print(e)

        return Response(response)


CreateJobPosting = CreateJobPosting.as_view()


class UpdateJobPosting(APIView):
    def post(self , request):
        response = {}
        response['status_code'] = 500
        response['message'] = 'Something went wrong'
        try:
            data = request.data
            print(data)
            job_position    = data.get('job_position')
            job_location    = data.get('job_location')
            job_description  = data.get('job_description')
            id = data.get('id')

            internal_job_posting_obj  = InternalJobPosting.objects.get(id = id)
            internal_job_posting_obj.position  = job_position
            internal_job_posting_obj.job_location  = job_location
            internal_job_posting_obj.job_description  = job_description

            internal_job_posting_obj.save()


            response['status_code'] = 200
            response['message'] = 'Job posting updated'
        except Exception as e:
            print(e)

        return Response(response)


UpdateJobPosting  = UpdateJobPosting.as_view()