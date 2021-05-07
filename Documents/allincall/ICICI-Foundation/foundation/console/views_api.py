# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import reset_queries
from django.http import response
# from accounts.views import pinocde

from django.http.response import JsonResponse

from rest_framework import authentication, permissions
from django.contrib.auth.models import User

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# Libraries
from django.shortcuts import render
from django.shortcuts import redirect, HttpResponse
from django.utils.dateparse import parse_date
from datetime import datetime

from src import settings

import sys

import json

# console.models import 
from .models import OTPVerification

from console.utils_api import *

# EasySTEPApp
import logging
logging.basicConfig()
logger = logging.getLogger(__name__)

#from fpdf import FPDF
from datetime import datetime

''' 
ADDED NEW IMPORTS HERE 
'''

from .utils import random_with_N_digits,send_otp_at_given_mobile_number,send_sms,distance


class GetBatchDetails(APIView):

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

        auth_header = request.META['HTTP_AUTHORIZATION']
        import base64
        encoded_credentials = auth_header.split(' ')[1]  # Removes "Basic " to isolate credentials
        decoded_credentials = base64.b64decode(encoded_credentials).decode("utf-8").split(':')
        username = decoded_credentials[0]
        password = decoded_credentials[1]

        response = {
            "status_code": 500,
            "message": "Internal server error"
            }
        try:
            if username != settings.API_ACCESS_USERNAME:
                response['status_code'] = 400
                response['message'] = "Invalid Access"
                raise Exception("Invalid Access")

            batch_id = request.data['batch_id']

            logger.info(f"[GetBatchDetails] BATCH ID - Received - {batch_id}")

            result = fetch_batch_details_from_db(batch_id)
            
            if result != None:
                response['status_code'] = 200
                response['message'] = "Success"
                response['details'] = result
            else:
                response['status_code'] = 400
                response['message'] = "Bad request"
                response['details'] = result

            response['batch_id'] = str(batch_id)


        except Exception as e:  # noqa: F841
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error(f"GetBatchDetails {str(e)} at {str(exc_tb.tb_lineno)}",)

        return Response(data=response)


GetBatchDetails = GetBatchDetails.as_view()


class GetEmployeeDetails(APIView):

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

        auth_header = request.META['HTTP_AUTHORIZATION']
        import base64
        encoded_credentials = auth_header.split(' ')[1]  # Removes "Basic " to isolate credentials
        decoded_credentials = base64.b64decode(encoded_credentials).decode("utf-8").split(':')
        username = decoded_credentials[0]
        password = decoded_credentials[1]
        print(username, password)

        response = {"status_code": 500, "message": "Internal server error"}
        try:

            if username != settings.API_ACCESS_USERNAME:
                response['status_code'] = 400
                response['message'] = "Invalid Access"
                raise Exception("Invalid Access")

            try:
                employee_id = request.data['employee_id']
            except Exception as e:
                employee_id = None

            print(f"BATCH ID - RECEIVED - {employee_id}")

            if employee_id:
                result = fetch_employee_details_from_db(employee_id)
            else:
                raise Exception("Blank/Invalid value passed")    
            
            if result != None:
                response['status_code'] = 200
                response['message'] = "Success"
                response['details'] = result
            else:
                response['status_code'] = 400
                response['message'] = "Bad request"
                response['details'] = result    

            response['employee_id'] = str(employee_id)

        except Exception as e:  # noqa: F841
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error(f"GetEmployeeDetails {str(e)} at {str(exc_tb.tb_lineno)}")

        return Response(data=response)


GetEmployeeDetails = GetEmployeeDetails.as_view()

class GetSkillAcademyDetails(APIView):

    authentication_classes = [SessionAuthentication, BasicAuthentication]

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

        auth_header = request.META['HTTP_AUTHORIZATION']
        import base64
        encoded_credentials = auth_header.split(' ')[1]  # Removes "Basic " to isolate credentials
        decoded_credentials = base64.b64decode(encoded_credentials).decode("utf-8").split(':')
        username = decoded_credentials[0]
        password = decoded_credentials[1]
        print(username, password)

        response = {"status_code": 500, "message": "Internal server error"}
        try:

            if username != settings.API_ACCESS_USERNAME:
                response['status_code'] = 400
                response['message'] = "Invalid Access"
                raise Exception("Invalid Access")

            try:
                isa_id = request.data['isa_id']
            except Exception as e:
                isa_id = None

            if isa_id:
                result = fetch_skill_academy_from_db(isa_id)
            else:
                raise Exception("Blank/Invalid value passed")    

            if result != None:
                response['status_code'] = 200
                response['message'] = "Success"
                response['details'] = result
            else:
                response['status_code'] = 400
                response['message'] = "Bad request"
                response['details'] = result    

            response['isa_id'] = str(isa_id)

        except Exception as e:  # noqa: F841
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error(f"GetSkillAcademyDetails {str(e)} at {str(exc_tb.tb_lineno)}")

        return Response(data=response)

GetSkillAcademyDetails = GetSkillAcademyDetails.as_view()

class GetEnrolledTraineeDetails(APIView):

    authentication_classes = [SessionAuthentication, BasicAuthentication]

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

        auth_header = request.META['HTTP_AUTHORIZATION']
        import base64
        encoded_credentials = auth_header.split(' ')[1]  # Removes "Basic " to isolate credentials
        decoded_credentials = base64.b64decode(encoded_credentials).decode("utf-8").split(':')
        username = decoded_credentials[0]
        password = decoded_credentials[1]

        response = {"status_code": 500, "message": "Internal server error"}
        try:

            if username != settings.API_ACCESS_USERNAME:
                response['status_code'] = 400
                response['message'] = "Invalid Access"
                raise Exception("Invalid Access")

            try:
                trainee_id = request.data['trainee_id']
            except Exception as e:
                trainee_id = None
            try:
                applicantion_id = request.data['application_id']
            except Exception as e:
                applicantion_id = None    

            if trainee_id or applicantion_id:
                result = fetch_enrolled_trainee_details_from_db(trainee_id,applicantion_id)
            else:
                raise Exception("Blank values in the parameters")
            
            if result != None:
                response['status_code'] = 200
                response['message'] = "Success"
                response['details'] = result
            else:
                response['status_code'] = 400
                response['message'] = "Bad request"
                response['details'] = result

        except Exception as e:  # noqa: F841
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error(f"GetBatchDetails {str(e)} at {str(exc_tb.tb_lineno)}")
            response['error'] = str(e)           

        return Response(data=response)


GetEnrolledTraineeDetails = GetEnrolledTraineeDetails.as_view()




class GetTraineeDetailsMobDob(APIView):

    authentication_classes = [SessionAuthentication, BasicAuthentication]

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

        auth_header = request.META['HTTP_AUTHORIZATION']
        import base64
        encoded_credentials = auth_header.split(' ')[1]  # Removes "Basic " to isolate credentials
        decoded_credentials = base64.b64decode(encoded_credentials).decode("utf-8").split(':')
        username = decoded_credentials[0]
        password = decoded_credentials[1]

        response = {"status_code": 500, "message": "Internal server error"}
        try:

            if username != settings.API_ACCESS_USERNAME:
                response['status_code'] = 400
                response['message'] = "Invalid Access"
                raise Exception("Invalid Access")

            try:
                mobile_number = request.data['mobile_number']
            except Exception as e:
                mobile_number = None
            try:
                dob = request.data['dob']
            except Exception as e:
                dob = None
            try:
                application_id = request.data['application_id']
            except Exception as e:
                application_id = None                
            
            if mobile_number or dob or application_id:
                result = fetch_trainee_details_from_db(mobile_number,dob,application_id)
            else:
                raise Exception("Blank values in the parameters")
            
            if result != None:
                response['status_code'] = 200
                response['message'] = "Success"
                response['details'] = result
            else:
                response['status_code'] = 400
                response['message'] = "Bad request"
                response['details'] = result

        except Exception as e:  # noqa: F841
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error(f"GetBatchDetails {str(e)} at {str(exc_tb.tb_lineno)}")
            response['error'] = str(e)

        return Response(data=response)


GetTraineeDetailsMobDob = GetTraineeDetailsMobDob.as_view()

###########################################

class GetEnrolledTraineeDetailsSummary(APIView):

    authentication_classes = [SessionAuthentication, BasicAuthentication]

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

        auth_header = request.META['HTTP_AUTHORIZATION']
        import base64
        encoded_credentials = auth_header.split(' ')[1]  # Removes "Basic " to isolate credentials
        decoded_credentials = base64.b64decode(encoded_credentials).decode("utf-8").split(':')
        username = decoded_credentials[0]
        password = decoded_credentials[1]

        response = {"status_code": 500, "message": "Internal server error"}
        try:

            if username != settings.API_ACCESS_USERNAME:
                response['status_code'] = 400
                response['message'] = "Invalid Access"
                raise Exception("Invalid Access")

            try:
                trainee_id = request.data['TraineeId']
            except Exception as e:
                trainee_id = None 
                response["status_code"] = 400
                response["message"] = "Invalid Trainee Id sent"
                            
            if trainee_id:
                result = fetch_enrolled_trainee_details_summary_from_db(trainee_id)
            else:
                raise Exception("Blank values in the parameters")
            if result != None:
                response['status_code'] = 200
                response['message'] = "Success"
                response['details'] = result
            else:
                response['status_code'] = 400
                response['message'] = "Bad request"
                response['details'] = result

            print(f"{username} got the correct access")

        except Exception as e:  # noqa: F841
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error(f"GetEnrolledTraineeDetailsSummary {str(e)} at {str(exc_tb.tb_lineno)}",)
            response['error'] = str(e)             

        return Response(data=response)


GetEnrolledTraineeDetailsSummary = GetEnrolledTraineeDetailsSummary.as_view()


import uuid

class SendMobileOTP(APIView):

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

        auth_header = request.META['HTTP_AUTHORIZATION']
        import base64
        encoded_credentials = auth_header.split(' ')[1]  # Removes "Basic " to isolate credentials
        decoded_credentials = base64.b64decode(encoded_credentials).decode("utf-8").split(':')
        username = decoded_credentials[0]
        password = decoded_credentials[1]
        print(username, password)

        response = {"status_code": 500, "message": "Internal server error"}
        try:

            if username != settings.API_ACCESS_USERNAME:
                response['status_code'] = 400
                response['message'] = "Invalid Access"
                raise Exception("Invalid Access")

            try:
                mobile_number = request.data['mobile_number']
            except Exception as e:
                mobile_number = None

            print(f"Mobile Number - RECEIVED - {mobile_number}")

            #OTP = random_with_N_digits(6)
            if mobile_number:
                OTP = send_otp_at_given_mobile_number(mobile_number)
                if OTP!=-1:
                    unique_otp_id = str(uuid.uuid4())
                    #print(f"Unique ID created for OTP being sent is {unique_otp_id}")
                    logger.info(f"Unique ID created for OTP being sent is {unique_otp_id}")
                    OTPVerification.objects.create(unique_otp_id = unique_otp_id, otp=OTP, mob_no = str(mobile_number))
                    response["status_code"] = 200
                    response["unique_otp_id"] = unique_otp_id
                    response["mob_no"] = mobile_number
                    response["message"] = "Success"
            else:    
                raise Exception("Invalid Mobile Number")

        except Exception as e:  # noqa: F841
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error(f"SendMobileOTP {str(e)} at {(exc_tb.tb_lineno)}")

        return Response(data=response)


SendMobileOTP = SendMobileOTP.as_view()


class SendEmailOTP(APIView):

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

        auth_header = request.META['HTTP_AUTHORIZATION']
        import base64
        encoded_credentials = auth_header.split(' ')[1]  # Removes "Basic " to isolate credentials
        decoded_credentials = base64.b64decode(encoded_credentials).decode("utf-8").split(':')
        username = decoded_credentials[0]
        password = decoded_credentials[1]
        print(username, password)

        response = {"status_code": 500, "message": "Internal server error"}
        try:

            if username != settings.API_ACCESS_USERNAME:
                response['status_code'] = 400
                response['message'] = "Invalid Access"
                raise Exception("Invalid Access")

            try:
                email_id = request.POST['email_id']
            except Exception as e:
                email_id = None

            print(f"Mobile Number - RECEIVED - {email_id}")

            #OTP = random_with_N_digits(6)
            if email_id:
                from console.utils import send_otp_mail, send_mail
                otp = random_with_N_digits(6)
                OTP = send_otp_mail(email_id,otp)
                if OTP!=-1 and OTP == otp:
                    unique_otp_id = str(uuid.uuid4())
                    #print(f"Unique ID created for OTP being sent is {unique_otp_id}")
                    logger.info(f"Unique ID created for OTP being sent is {unique_otp_id}")
                    OTPVerification.objects.create(unique_otp_id = unique_otp_id, otp=OTP, email_id = str(email_id))
                    response["status_code"] = 200
                    response["unique_otp_id"] = unique_otp_id
                    response["email_id"] = email_id
                    response["message"] = "Success"
            else:    
                raise Exception("Invalid Email ID Number")

        except Exception as e:  # noqa: F841
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error(f"SendEmailOTP {str(e)} at {(exc_tb.tb_lineno)}")


        return Response(data=response)


SendEmailOTP = SendEmailOTP.as_view()

class VerifyOTP(APIView):

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

        auth_header = request.META['HTTP_AUTHORIZATION']
        import base64
        encoded_credentials = auth_header.split(' ')[1]  # Removes "Basic " to isolate credentials
        decoded_credentials = base64.b64decode(encoded_credentials).decode("utf-8").split(':')
        username = decoded_credentials[0]
        password = decoded_credentials[1]
        print(username, password)

        response = {"status_code": 500, "message": "Internal server error"}
        try:

            if username != settings.API_ACCESS_USERNAME:
                response['status_code'] = 400
                response['message'] = "Invalid Access"
                raise Exception("Invalid Access")

            try:
                unique_otp_id = request.POST['unique_otp_id']
            except Exception as e:
                unique_otp_id = None

            try:
                otp = request.POST['otp']
            except Exception as e:
                otp = None    

            #print(f"Unique OTP id - RECEIVED - {unique_otp_id} and OTP received - {otp}")
            logger.info(f"Unique OTP id - RECEIVED - {unique_otp_id} and OTP received - {otp}")


            #OTP = random_with_N_digits(6)
            if unique_otp_id and otp:
                    otp_obj  = OTPVerification.objects.filter(unique_otp_id=unique_otp_id).order_by('-pk')
                    if otp_obj[0]:
                        print(f"Actual OTP {otp_obj[0].otp} Received OTP {otp}")
                        if otp_obj[0].otp == otp:
                            response["status_code"] = 200
                            response["message"] = "Success"
                            response["description"] = "OTP verified successfully"
                        else:
                            response["status_code"] = 300
                            response["message"] = "Failure"
                            response["description"] = "Invalid OTP entered by user"

            else:    
                raise Exception("Invalid Values entered")

        except Exception as e:  # noqa: F841
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error(f"VerifyOTP {str(e)} at {(exc_tb.tb_lineno)}")

           

        return Response(data=response)


VerifyOTP = VerifyOTP.as_view()


        

class SubmitTraineeApplication(APIView):

    authentication_classes = [SessionAuthentication, BasicAuthentication]

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

        auth_header = request.META['HTTP_AUTHORIZATION']
        import base64
        encoded_credentials = auth_header.split(' ')[1]  # Removes "Basic " to isolate credentials
        decoded_credentials = base64.b64decode(encoded_credentials).decode("utf-8").split(':')
        username = decoded_credentials[0]
        password = decoded_credentials[1]
        print(username, password)

        response = {"status_code": 500, "message": "Internal server error"}
        try:

            if username != settings.API_ACCESS_USERNAME:
                response['status_code'] = 400
                response['message'] = "Invalid Access"
                raise Exception("Invalid Access")

            ##### Parsing data from the packet received from the API
            required_keys = ["FY","Salutation","TraineeName","ISAId","ISAName","Gender","DateOfBirth","PhoneNo","Email","Education","InterestedCourseId","InterestedCourseName"]
            rv = {}
            a = ""
            for key in required_keys:
                try:
                    temp = request.POST[key]
                except Exception as e:
                    response["status_code"] = 400
                    response["message"] = f"Missing value(s) in input packet - {key}."
                    raise Exception("Missing required fields")
                rv[key] = temp
            
            rv['CreatedOn'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            #print(f"Details RECEIVED - {json.dumps(rv)}")
            logger.info(f"Details RECEIVED - {json.dumps(rv)}")

            status, message = check_input_trainee_application(rv)
            print(f"here is the status - {status} with messsage = {message}")
            if not status:
                response["status_code"] = 403
                response["message"] = f"Missing/Invalid value(s) in input packet - {message}."
                raise Exception(f"Missing/Invalid value(s) in input packet - {message}.")
            ######### Fetching data from server

            from django.db import connections
            cursor = connections['icici'].cursor()
            command = f"select ApplicationId from l7_traineeapplications where ApplicationId like '{rv['FY']}{rv['ISAId']}%' order by ApplicationId DESC limit 1;"
            qs = cursor.execute(command)
            rows = cursor.fetchall()
            cols = ["ApplicationId"]
            result_id = [dict(zip(cols, row)) for row in rows]
            cursor.close
            latest_application_number = result_id[0]["ApplicationId"]
            #print(f"Latest Application No. is {latest_application_number}")
            logger.info(f"Latest Application No. is {latest_application_number}")
            new_application_number = int(latest_application_number) + 1

            #print(f"New Application No. is {new_application_number}")
            logger.info(f"New Application No. is {new_application_number}")


            command = f"""insert into l7_traineeapplications 
                        (ApplicationId,FY,Salutation,TraineeName,ISAId,ISAName,
                        InterestedCourseId,InterestedCourseName,Gender,DateOfBirth,
                        PhoneNo,Email,Education,CreatedOn) 
                        values 
                        ({new_application_number},{rv['FY']},{rv['Salutation']},"{rv['TraineeName']}",{rv['ISAId']},"{rv['ISAName']}",
                        {rv['InterestedCourseId']},"{rv['InterestedCourseName']}",{rv['Gender']},"{rv['DateOfBirth']}",
                        {rv['PhoneNo']},"{rv['Email']}","{rv['Education']}","{rv['CreatedOn']}");"""

            command = command.replace("\n","")
            command = " ".join(command.split())
            cursor = connections['icici'].cursor()
            qs = cursor.execute(command)
            cursor.close
            if qs == 1:
                logger.info(f"Entry with ApplicationId - {new_application_number} written in database successfully")
                response['status_code'] = 200
                response['message'] = "Success"
                response['details'] = rv
                response['application_id'] = new_application_number

        except Exception as e:  # noqa: F841
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error(f"SubmitTraineeApplication {str(e)} at {(exc_tb.tb_lineno)}")
            if "Duplicate entry" in str(e):
                response['status_code'] = 400
                response['message'] = str(e)

        return Response(data=response)


SubmitTraineeApplication = SubmitTraineeApplication.as_view()


# def check_input_enrolled_trainee_application(rv):
#     from .constants import course_id_dict,isa_id_dict,education_type_list, guardian_type_list, caste_type_list, religion_type_list, disability_type_list, annual_household_income_type_list,marital_status_type_list
#     if len(str(rv["ApplicationId"])) != 10:
#         return False,"Invalid ApplicationId value. Permissible ApplicationId value contains 10 digits."

#     elif len(str(rv["BatchId"])) != 9:
#         return False,"Invalid BatchId value. Permitted Values is of 9 digits "

#     elif len(str(rv["ISACourseId"])) not in [5]:
#         return False,"Invalid  ISACourseId value. Permitted value is of 5 digits. Please one leading 0 to make it 5 digit."

#     elif int(str(rv["ISACourseId"])[-2:]) < 1 or int(str(rv["ISACourseId"])[-2:]) > 31:
#         return False,"Invalid CourseId in ISACourseId"

#     elif int(str(rv["ISACourseId"])[:3]) < 1 or int(str(rv["ISACourseId"])[-2:]) > 30:
#         return False,"Invalid ISAId in ISACourseId"    

#     elif int(rv["Gender"]) != 1 and int(rv["Gender"]) != 2 and int(rv["Gender"]) != 3:
#         return False,"Invalid Gender value. Permitted Values 1-(Male), 2-(Female), 3-(Transgender)"

#     elif int(rv["SameAsPermanentAddress"]) not in [1,0]:
#         return False,"Invalid SameAsPermanentAddress value. Permitted Values 1-(Yes), 0-(No)"

#     if len(str(rv["PPinCode"])) != 6:
#         return False,"Invalid PPinCode value. Permissible PPinCode value contains 6 digits."

#     elif rv["MaritalStatus"] not in marital_status_type_list:
#         return False,"Invalid MaritalStatus value. Permitted values are Single, Unmarried, Married, Divorced, Widow"

#     elif rv["GuardianType"] not in guardian_type_list:
#         return False,"Invalid GuardianType value. Permitted values are S/o, D/o, W/o, C/o"

#     elif rv["Caste"] not in caste_type_list:
#         return False,"Invalid Caste value. Permitted values are General, SC, ST, OBC, PH, Others"

#     elif rv["Religion"] not in religion_type_list:
#         return False,"Invalid Religion value. Permitted values are Hindu, Muslim, Sikh, Jew, Christian, Buddhist, Jain, Others" 

#     elif rv["DisabilityType"] not in disability_type_list:
#         return False,"Invalid DisabilityType value. Permitted values are None, Blindness (Visually Impaired)), Locomotor Disability, Deaf, Low Vision, Hard of Hearing, Intellectual Disability, Autism Spectrum Disorder, Specific Learning Disabilities, Speech and Language Disability, Cerebral Palsy, Deaf and Blindness, Mental Behaviour,Mental Illness ,Mental Retardation, Leprosy Cured Patient, Acid Attack Victim, Dwarfism, Hemophilia, Thalassemia, Sickle Cell Disease, Multiple Sclerosis, Muscular Dystrophy, Parkinson Disease"

#     elif int(rv["PreTrainingStatus"]) not in [1,2]:
#         return False,"Invalid PreTrainingStatus value. Permitted Values 1-(Fresher), 2-(Experienced)"

#     elif rv["EducationLevel"] not in education_type_list:
#         return False,"Invalid EducationLevel value. Permitted values are Uneducated, Upto 4th, 5th to 8th, 9th to 10th , 11th to 12th , Undergraduate, Postgraduate, ITI, Polytechnic, Diploma"

#     elif int(rv["AnnualHouseholdIncome"]) not in [1,2,3]:
#         return False,"Invalid AnnualHouseholdIncome value. Permitted Values 1-(96 Thousand–2.5lakhs), 2-(Below 96 Thousand), 3-(Above 2.5 lakhs)"                 

#     elif int(rv["BelowPovertyLine"]) not in [1,2]:
#         return False,"Invalid BelowPovertyLine value. Permitted Values 1-Yes or 2-No"

#     else:
#         return True, "Successfully Verified"

class SubmitEnrollmentTraineeApplication(APIView):

    authentication_classes = [SessionAuthentication, BasicAuthentication]

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

        auth_header = request.META['HTTP_AUTHORIZATION']
        import base64
        encoded_credentials = auth_header.split(' ')[1]  # Removes "Basic " to isolate credentials
        decoded_credentials = base64.b64decode(encoded_credentials).decode("utf-8").split(':')
        username = decoded_credentials[0]
        password = decoded_credentials[1]
        print(username, password)

        response = {"status_code": 500, "message": "Internal server error"}
        try:

            if username != settings.API_ACCESS_USERNAME:
                response['status_code'] = 400
                response['message'] = "Invalid Access"
                raise Exception("Invalid Access")

            ##### Parsing data from the packet received from the API
            required_keys = ["ApplicationId",
                            "PAddress","PDistrictId","PDistrict","PStateId","PState","PTownCity","PPinCode","PCountryId","PCountry",
                            "SameAsPermanentAddress",
                            "Address","DistrictId","District","StateId","State","TownCity","PINCode","CountryId","Country",
                            "PlaceOfBirth","MaritalStatus","GuardianType","FathersName","GuardianName","MotherMaidenName",
                            "Caste","Religion","DisabilityType","PreTrainingStatus","NoOfMonthsOfPreviousExperience",
                            "EducationLevel","BelowPovertyLine","AnnualHouseholdIncome"]

            if request.POST["SameAsPermanentAddress"] in [1,"1"]:
                required_keys = ["ApplicationId",
                            "PAddress","PDistrictId","PDistrict","PStateId","PState","PTownCity","PPinCode","PCountryId","PCountry",
                            "SameAsPermanentAddress",
                            "PlaceOfBirth","MaritalStatus","GuardianType","FathersName","GuardianName","MotherMaidenName",
                            "Caste","Religion","DisabilityType","PreTrainingStatus","NoOfMonthsOfPreviousExperience",
                            "EducationLevel","BelowPovertyLine","AnnualHouseholdIncome"]                
            rv = {}
            a = ""
            for key in required_keys:
                try:
                    temp = request.POST[key]
                except Exception as e:
                    response["status_code"] = 400
                    response["message"] = f"Missing value(s) in input packet - {key}."
                    raise Exception("Missing required fields")
                rv[key] = temp
            
            if request.POST["SameAsPermanentAddress"] in [1,"1"]:
                rv['Address'] = rv['PAddress']
                rv['DistrictId'] = rv['PDistrictId']
                rv['District'] = rv['PDistrict']
                rv['StateId'] = rv['PStateId']
                rv['State'] = rv['PState']
                rv['TownCity'] = rv['PTownCity']
                rv['PINCode'] = rv['PPinCode']
                rv['District'] = rv['PDistrict']
                rv['CountryId'] = rv['PCountryId']
                rv['Country'] = rv['PCountry']

            rv['CreatedOn'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            #print(f"Details RECEIVED - {json.dumps(rv)}")
            logger.info(f"Details RECEIVED - {json.dumps(rv)}")
            
            
            

            ######### Fetching Application data from server

            from django.db import connections
            cursor = connections['icici'].cursor()
            command = f"select ApplicationId, TraineeName, ISAId, SuggestedCourseId, SuggestedCourseName, BatchId, Gender from l7_traineeapplications where ApplicationId={rv['ApplicationId']};"
            print(command)
            qs = cursor.execute(command)
            if qs == 1:
                rows = cursor.fetchall()
                cols = ["ApplicationId", "TraineeName", "ISAId", "SuggestedCourseId", "SuggestedCourseName", "BatchId", "Gender"]
                result_id = [dict(zip(cols, row)) for row in rows]
                print(result_id)
                cursor.close
                rv["TraineeName"] = result_id[0]["TraineeName"]
                rv["BatchId"] = result_id[0]["BatchId"]
                if result_id[0]["Gender"] == "Male":
                    rv["Gender"] = 1
                elif result_id[0]["Gender"] == "Female":
                    rv["Gender"] = 2
                elif result_id[0]["Gender"] == "Transgender":
                    rv["Gender"] = 3
                
                rv["BatchId"] = result_id[0]["BatchId"]
                rv["Course"] = result_id[0]["SuggestedCourseName"]
                rv["ISACourseId"] = str(result_id[0]["ISAId"]).zfill(3) + str(result_id[0]["SuggestedCourseId"]).zfill(2)
            else:
                cursor.close
                raise Exception("Couldn't find the such details of such ApplicationId")


            status, message = check_input_enrolled_trainee_application(rv)
            print(f"here is the status - {status} with messsage = {message}")
            if not status:
                response["status_code"] = 403
                response["message"] = f"Missing / Invalid value(s) in the input packet - {message}."
                raise Exception(f"Missing/Invalid value(s) in input packet - {message}.")

            from console.constants import isa_center_head
            a = isa_center_head[str(rv["ISACourseId"][1:3])]
            print(a)
            rv['ApproverRoleLvl1'] = f"_{a}_"
            
            ######### Fetching TraineeID data from server

            from django.db import connections
            cursor = connections['icici'].cursor()
            command = f"select TraineeId from l7_enrldtraineeapplication where TraineeId like '{rv['BatchId']}%' order by TraineeId DESC limit 1;"
            print(command)
            qs = cursor.execute(command)
            if qs == 1:
                rows = cursor.fetchall()
                cols = ["TraineeId"]
                result_id = [dict(zip(cols, row)) for row in rows]
                print(result_id)
                cursor.close
                latest_enrollment_number = result_id[0]["TraineeId"]
            else:
                latest_enrollment_number = rv['BatchId'] + "00"
            print(f"****************\nLatest Enrollment No. is {latest_enrollment_number}\n************\n")
            new_enrollment_number = int(latest_enrollment_number) + 1
            print(f"\n************\nNew Enrollment No. is {new_enrollment_number}\n************\n")

            command = f"""insert into l7_enrldtraineeapplication 
                        (TraineeId,ISACourseId,Course,BatchId,ApplicationId,TraineeName,Gender,
                        PAddress,PDistrictId,PDistrict,PStateId,PState,PTownCity,PPinCode,PCountryId,PCountry,
                        SameAsPermanentAddress,
                        Address,DistrictId,District,StateId,State,TownCity,PINCode,CountryId,Country,
                        PlaceOfBirth,MaritalStatus,GuardianType,FathersName,GuardianName,MotherMaidenName,
                        Caste,Religion,DisabilityType,PreTrainingStatus,NoOfMonthsOfPreviousExperience,
                        EducationLevel,BelowPovertyLine,AnnualHouseholdIncome,CreatedOn,ApproverRoleLvl1,ApprovalStatusLvl1) 
                        values 
                        ({new_enrollment_number},{rv['ISACourseId']},"{rv['Course']}",{rv['BatchId']},{rv['ApplicationId']},"{rv['ApplicationId']} - {rv['TraineeName']}",{rv['Gender']},
                        "{rv['PAddress']}",{rv['PDistrictId']},"{rv['PDistrict']}",{rv['PStateId']},"{rv['PState']}","{rv['PTownCity']}",{rv['PPinCode']},{rv['PCountryId']},"{rv['PCountry']}",
                        {rv['SameAsPermanentAddress']},
                        "{rv['Address']}",{rv['DistrictId']},"{rv['District']}",{rv['StateId']},"{rv['State']}","{rv['TownCity']}",{rv['PINCode']},{rv['CountryId']},"{rv['Country']}",
                        "{rv['PlaceOfBirth']}", "{rv['MaritalStatus']}","{rv['GuardianType']}", "{rv['FathersName']}","{rv['GuardianName']}", "{rv['MotherMaidenName']}",
                        "{rv['Caste']}", "{rv['Religion']}","{rv['DisabilityType']}", {rv['PreTrainingStatus']},"{rv['NoOfMonthsOfPreviousExperience']}",
                        "{rv['EducationLevel']}",{rv['BelowPovertyLine']},{rv['AnnualHouseholdIncome']}, "{rv['CreatedOn']}","{rv['ApproverRoleLvl1']}",2);"""

            command = command.replace("\n","")
            command = " ".join(command.split())
            cursor = connections['icici'].cursor()
            qs = cursor.execute(command)
            cursor.close
            if qs == 1:
                logger.info(f"Entry with TraineeId - {new_enrollment_number} written in database successfully")
                response['status_code'] = 200
                response['message'] = "Success"
                response['details'] = rv
                response['TraineeId'] = new_enrollment_number

        except Exception as e:  # noqa: F841
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error(f"SubmitEnrollmentTraineeApplication {str(e)} at {(exc_tb.tb_lineno)}")
            if "Duplicate entry" in str(e):
                response['status_code'] = 400
                response['message'] = str(e)

        return Response(data=response)


SubmitEnrollmentTraineeApplication = SubmitEnrollmentTraineeApplication.as_view()






################## follow-up application


class SubmitFollowUpEnrolledTrainee(APIView):

    authentication_classes = [SessionAuthentication, BasicAuthentication]

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

        auth_header = request.META['HTTP_AUTHORIZATION']
        import base64
        encoded_credentials = auth_header.split(' ')[1]  # Removes "Basic " to isolate credentials
        decoded_credentials = base64.b64decode(encoded_credentials).decode("utf-8").split(':')
        username = decoded_credentials[0]
        password = decoded_credentials[1]
        print(username, password)

        response = {"status_code": 500, "message": "Internal server error"}
        try:

            if username != settings.API_ACCESS_USERNAME:
                response['status_code'] = 400
                response['message'] = "Invalid Access"
                raise Exception("Invalid Access")

            ##### Parsing data from the packet received from the API

            rv = {}

            if request.POST["WorkingStatus"] in [1,"1"]:
                required_keys = ["TraineeId",
                            "WorkingStatus","WorkingLocation",
                            "MonthlySalary"]
                rv["ReasonIfNotWorking"] = ""
                rv["OtherReason"] = ""     
            elif request.POST["WorkingStatus"] in [2,"2"]:
                rv["WorkingLocation"] = ""
                rv["MonthlySalary"] = ""
                if request.POST["ReasonIfNotWorking"] in [13,"13"]:
                    required_keys = ["TraineeId",
                            "WorkingStatus","ReasonIfNotWorking","OtherReason",
                            ]
                else:
                    required_keys = ["TraineeId",
                            "WorkingStatus","ReasonIfNotWorking",
                            ]
                    rv["OtherReason"] = ""

            
            a = ""
            for key in required_keys:
                try:
                    temp = request.POST[key]
                except Exception as e:
                    response["status_code"] = 400
                    response["message"] = f"Missing value(s) in input packet - {key}."
                    raise Exception("Missing required fields")
                rv[key] = temp

            rv['CreatedOn'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            rv['FollowupExecutive'] = 2
            rv['CallerName'] = "Chatbot API"
            rv['ParentsInformedIfNotWorking'] = ""

            print(f"Details RECEIVED - {json.dumps(rv)}")
                       

            ######### Fetching Application data from server

            from django.db import connections
            cursor = connections['icici'].cursor()
            command = f"select l7_enrldtraineeapplication.TraineeName, l7_enrldtraineeapplication.BatchId, l7_enrldtraineeapplication.ApplicationId, BatchName, PhoneNo from l7_traineeapplications join l7_enrldtraineeapplication where l7_enrldtraineeapplication.ApplicationId=l7_traineeapplications.ApplicationId  and l7_enrldtraineeapplication.TraineeId={rv['TraineeId']};"
            print(command)
            qs = cursor.execute(command)
            if qs == 1:
                rows = cursor.fetchall()
                cols = ["TraineeName", "BatchId",  "ApplicationId","BatchName","PhoneNo"]
                result_id = [dict(zip(cols, row)) for row in rows]
                print(result_id)
                cursor.close
                rv["TraineeName"] = result_id[0]["TraineeName"]
                rv["BatchId"] = result_id[0]["BatchId"]
                rv["ApplicationId"] = result_id[0]["ApplicationId"]
                rv["BatchName"] = result_id[0]["BatchName"]
                rv["PhoneNo"] = result_id[0]["PhoneNo"]

            else:
                cursor.close
                raise Exception(f"Couldn't find details of TraineeId-{rv['TraineeId']} in Enrolled Trainee Applications")

            print(rv)

            status, message = check_input_follow_up_enrolled_trainee(rv)
            print(f"here is the status - {status} with messsage = {message}")
            if not status:
                response["status_code"] = 403
                response["message"] = f"Missing / Invalid value(s) in the input packet - {message}."
                raise Exception(f"Missing/Invalid value(s) in input packet - {message}.")

            
            ######### Fetching TraineeID data from server

            from django.db import connections
            cursor = connections['icici'].cursor()
            command = f"select FollowUpNumber from l8_followup where TraineeId={rv['TraineeId']} order by FollowUpNumber DESC limit 1;"
            print(command)
            qs = cursor.execute(command)
            if qs == 1:
                rows = cursor.fetchall()
                cols = ["FollowUpNumber"]
                result_id = [dict(zip(cols, row)) for row in rows]
                print(result_id)
                cursor.close
                latest_follow_up_number = result_id[0]["FollowUpNumber"]
            else:
                latest_follow_up_number = 0
            print(f"****************\nLatest follow-up No. is {latest_follow_up_number}\n************\n")
            new_follow_up_number = int(latest_follow_up_number) + 1
            print(f"\n************\nNew follow_up No. is {new_follow_up_number}\n************\n")

            command = f"""insert into l8_followup 
                        (TraineeId,TraineeName,BatchId,BatchName,
                        PhoneNo,FollowUpNumber,WorkingStatus,ParentsInformedIfNotWorking,
                        ReasonIfNotWorking,OtherReason,WorkingLocation,MonthlySalary,
                        FollowupExecutive,CallerName,CreatedOn
                        ) 
                        values 
                        ({rv['TraineeId']},"{rv['TraineeName']}",{rv['BatchId']},"{rv['BatchName']}",
                        "{rv['PhoneNo']}",{new_follow_up_number},{rv['WorkingStatus']},"{rv['ParentsInformedIfNotWorking']}",
                        "{rv['ReasonIfNotWorking']}","{rv['OtherReason']}","{rv['WorkingLocation']}","{rv['MonthlySalary']}",
                        "{rv['FollowupExecutive']}","{rv['CallerName']}",
                        "{rv['CreatedOn']}");"""

            print(command)
            command = command.replace("\n","")
            command = " ".join(command.split())
            print(command)
            cursor = connections['icici'].cursor()
            qs = cursor.execute(command)
            cursor.close
            if qs == 1:
                logger.info(f"Entry with TraineeId - {rv['TraineeId']} with FollowUpNumber-{new_follow_up_number} written in l8_followup table successfully")
                response['status_code'] = 200
                response['message'] = "Success"
                response['details'] = rv
                response['TraineeId'] = rv['TraineeId']
                response['FollowUpNumber'] = {new_follow_up_number}


        except Exception as e:  # noqa: F841
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("SubmitFollowUpEnrolledTrainee %s at %s",
                         str(e), str(exc_tb.tb_lineno))
            if "Duplicate entry" in str(e):
                response['status_code'] = 400
                response['message'] = str(e)

        return Response(data=response)


SubmitFollowUpEnrolledTrainee = SubmitFollowUpEnrolledTrainee.as_view()



##########################################


# def send_sms(mobile_number, message):
#     url=f"http://api.equence.in/pushsms?username=icici_found_otp&password=-EN20-sa&to=91{mobile_number}&from=IFOUND&text={message}"
#     #url=f"http://api.equence.in/pushsms?username=icici_found_otp&password=-EN20-sa&to=91{mobile_number}&from=IFOUND&text={message} ."
#     print(url)
#     r= requests.get(url=url)
#     json_data = json.loads(r.text)
#     print(json_data)
#     logger.info(json_data)
#     if json_data["response"][0]["status"] == "success":
#         print("message sent successfully")
#         return True
#     else:
#         return False


class SubmitReferral(APIView):

    authentication_classes = [SessionAuthentication, BasicAuthentication]

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

        auth_header = request.META['HTTP_AUTHORIZATION']
        import base64
        encoded_credentials = auth_header.split(' ')[1]  # Removes "Basic " to isolate credentials
        decoded_credentials = base64.b64decode(encoded_credentials).decode("utf-8").split(':')
        username = decoded_credentials[0]
        password = decoded_credentials[1]
        print(username, password)

        response = {"status_code": 500, "message": "Internal server error"}
        try:

            if username != settings.API_ACCESS_USERNAME:
                response['status_code'] = 400
                response['message'] = "Invalid Access"
                raise Exception("Invalid Access")

            required_keys = ["referrer_name","referrer_mobile",
                            "referee_name","referee_mobile","referee_email",
                            "source"]
            rv = {}

            for key in required_keys:
                try:
                    temp = request.POST[key]
                except Exception as e:
                    response["status_code"] = 400
                    response["message"] = f"Missing value(s) in input packet - {key}."
                    raise Exception("Missing required fields")
                rv[key] = temp
  
                
            print(f"Details RECEIVED - {json.dumps(rv)}")
            
            from console.models import Referral

            temp = Referral.objects.create(
                referrer_name   =rv["referrer_name"],
                referrer_mobile =rv["referrer_mobile"],
                referee_name    =rv["referee_name"],
                referee_mobile  =rv["referee_mobile"],
                referee_email   =rv["referee_email"],
                source          =rv["source"]
            )

            response["status_code"]=300
            response["message"]="Object created but message not sent yet."

            referrer_msg = f"Thank you for referring {temp.referee_name}, for undergoing a training at ICICI Academy for Skills. Our team shall soon get in touch with them very soon. [Non OTP message]"
            referee_msg  = f"You have been referred by {temp.referrer_name}, for undergoing a training at ICICI Academy for Skills. Please click on link to enrol/enquire: <link>. [Non OTP message]"

            print(referrer_msg)
            print(referee_msg)

            referrer_msg_status = send_sms(temp.referrer_mobile,referrer_msg)
            referee_msg_status  = send_sms(temp.referee_mobile,referee_msg)

            if referrer_msg_status and referee_msg_status:
                response["status_code"]=200
                response["message"]="Message sent successfully to both referrer and referee" 


        except Exception as e:  # noqa: F841
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error(f"SubmitReferralAPI {str(e)} at {str(exc_tb.tb_lineno)}")

        return Response(data=response)


SubmitReferral = SubmitReferral.as_view()


from .helpers import *

class NearestAcademy(APIView):

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):

        auth_header = request.META['HTTP_AUTHORIZATION']
        import base64
        encoded_credentials = auth_header.split(' ')[1]  # Removes "Basic " to isolate credentials
        decoded_credentials = base64.b64decode(encoded_credentials).decode("utf-8").split(':')
        username = decoded_credentials[0]
        password = decoded_credentials[1]

        response = {"status_code": 500, "message": "Internal server error"}

        try:
            error = ""
            if username != settings.API_ACCESS_USERNAME:
                response['status_code'] = 400
                response['message'] = "Invalid Access"
                raise Exception("Invalid Access")
            try:
                pincode = request.data['pincode']                
                if len(str(pincode)) != 6:
                    error = "Please enter valid pincode value of only 6 digits"
                try:    
                    pincode =  int(str(pincode))
                except Exception as e:
                    error = "Please enter valid pincode value consisting of NUMERIC 6 digits"
            except Exception as e:
                pincode = None
   

            logger.info(f"Pincode - RECEIVED - {pincode}")
        
            from .constants import isa_academy_pincodes

            if pincode is None or error:
                response["status_code"]=400
                response["message"]="Error in input values"
                raise Exception(f"{error}")

            result = {}
            user_lat = ""
            user_lon =""

            if not check_pincode_exists(pincode):
                response['status_code'] = 400
                response['message'] = "Not a valid pincode from INDIA"
                raise Exception("Not a valid pincode of INDIA")
        
            zipcode = int(pincode)
            
            location = get_pincode_details(pincode)
            user_lat = float(location.get('lat'))
            user_lon = float(location.get('lon'))


            dist = []
            for pi in isa_academy_pincodes:
                key = list(pi.keys())[0]
                pi_obj = pi[key]
                print(f"""
                {float(pi_obj['Xlat'])} , {float(pi_obj['Ylong'])}, {user_lat} ,{user_lon}
                """)
                dis = distance(float(pi_obj['Xlat']),float(pi_obj['Ylong']),user_lat,user_lon)
                dist.append({'pincode' : pi  , 'km' : int(dis) })
                print(dis)
            dist = sorted(dist , key=lambda i:i ['km'])

            result = dist

            ######### Fetching TraineeID data from server

            from django.db import connections
            cursor = connections['icici'].cursor()
            command1 = f"""
            select l4_skillacademies.ISAId, l4_skillacademies.ISAName,
            l4_skillacademies.BuildingName,l4_skillacademies.Address1,
            l4_skillacademies.District,l4_skillacademies.State,
            l4_skillacademies.PinCode,
            l4_skillacademies.XCoordinateOfTheAcademy,l4_skillacademies.YCoordinateOfTheAcademy
            from l4_skillacademies where PinCode={list(result[0]["pincode"].keys())[0]};
            """
            command2 = f"""
            select l4_skillacademies.ISAId, l4_skillacademies.ISAName,
            l4_skillacademies.BuildingName,l4_skillacademies.Address1,
            l4_skillacademies.District,l4_skillacademies.State,
            l4_skillacademies.PinCode,
            l4_skillacademies.XCoordinateOfTheAcademy,l4_skillacademies.YCoordinateOfTheAcademy
            from l4_skillacademies where PinCode={list(result[1]["pincode"].keys())[0]};
            """
            command3 = f"""
            select l4_skillacademies.ISAId, l4_skillacademies.ISAName,
            l4_skillacademies.BuildingName,l4_skillacademies.Address1,
            l4_skillacademies.District,l4_skillacademies.State,
            l4_skillacademies.PinCode,
            l4_skillacademies.XCoordinateOfTheAcademy,l4_skillacademies.YCoordinateOfTheAcademy
            from l4_skillacademies where PinCode={list(result[2]["pincode"].keys())[0]};
            """
            

            
            qs = cursor.execute(command1)
            rows = cursor.fetchall()
            cols = [col[0] for col in cursor.description]
            result1 = [dict(zip(cols, row)) for row in rows]
           
            ''' GOT ERROR SO COMMENTED FOR DISCUSS - ABHIJEET '''
            #result1["map_link"] = f"""http://maps.google.com/maps?q={result1[0]["XCoordinateOfTheAcademy"]},{result1[0]["YCoordinateOfTheAcademy"]}"""
            
            
            cursor.close

            qs = cursor.execute(command2)
            rows = cursor.fetchall()
            cols = [col[0] for col in cursor.description]
            result2 = [dict(zip(cols, row)) for row in rows]
            cursor.close

            qs = cursor.execute(command3)
            rows = cursor.fetchall()
            cols = [col[0] for col in cursor.description]
            result3 = [dict(zip(cols, row)) for row in rows]
            cursor.close
    
            
            response['status_code'] = 200
            response['message'] = "Success"
            response['details'] = [
                {"first": result1[0], "distance": result[0]["km"]},
                {"second": result2[0], "distance": result[1]["km"]},
                {"third": result3[0],"distance":result[2]["km"]},
            ]



        except Exception as e:  # noqa: F841
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error(f"NearestAcademy {str(e)} at {str(exc_tb.tb_lineno)}")
            response["error"]  = str(e)            

        return Response(data=response)


NearestAcademy = NearestAcademy.as_view()




class GetBatchList(APIView):

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

        auth_header = request.META['HTTP_AUTHORIZATION']
        import base64
        encoded_credentials = auth_header.split(' ')[1]  # Removes "Basic " to isolate credentials
        decoded_credentials = base64.b64decode(encoded_credentials).decode("utf-8").split(':')
        username = decoded_credentials[0]
        password = decoded_credentials[1]

        response = {
            "status_code": 500,
            "message": "Internal server error"
            }
        try:
            if username != settings.API_ACCESS_USERNAME:
                response['status_code'] = 400
                response['message'] = "Invalid Access"
                raise Exception("Invalid Access")

            emp_id = request.data['emp_python3.6 -m venv venvid']

            logger.info(f"[GetBatchList] Employee ID - Received - {emp_id}")

            try:
                from django.db import connections
                cursor = connections['icici'].cursor()
                command = f"SELECT * FROM batchcalendar WHERE EmpId=\"{emp_id}\";"
                logger.info(f"[GetBatchList] SQL Command: {command}")
                qs = cursor.execute(command)
                rows = cursor.fetchall()
                cols = [col[0] for col in cursor.description]
                result = [dict(zip(cols, row)) for row in rows]
                cursor.close
                logger.info(f"[GetBatchList] SQL Result: {result}")

            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                logger.error(f"GetBatchList {str(e)} at {str(exc_tb.tb_lineno)}")
                logger.info(f"[GetBatchList] SQL Result: {None}")
                return None
           
            if result != None:
                response['status_code'] = 200
                response['message'] = "Success"
                response['details'] = result
            else:
                response['status_code'] = 400
                response['message'] = "Bad request"
                response['details'] = result

            response['emp_id'] = str(emp_id)


        except Exception as e:  # noqa: F841
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("GetBatchList %s at %s",
                         str(e), str(exc_tb.tb_lineno))

        return Response(data=response)


GetBatchList = GetBatchList.as_view()


class GetTraineeInBatch(APIView):

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

        auth_header = request.META['HTTP_AUTHORIZATION']
        import base64
        encoded_credentials = auth_header.split(' ')[1]  # Removes "Basic " to isolate credentials
        decoded_credentials = base64.b64decode(encoded_credentials).decode("utf-8").split(':')
        username = decoded_credentials[0]
        password = decoded_credentials[1]

        response = {
            "status_code": 500,
            "message": "Internal server error"
            }
        try:
            if username != settings.API_ACCESS_USERNAME:
                response['status_code'] = 400
                response['message'] = "Invalid Access"
                raise Exception("Invalid Access")

            batch_id = request.data['batch_id']

            logger.info(f"[GetTraineeInBatch] Employee ID - Received - {batch_id}")

            try:
                from django.db import connections
                cursor = connections['icici'].cursor()
                command = f"SELECT TraineeId, ApplicationId, TraineeName, BatchId, ISACourseId FROM l7_enrldtraineeapplication WHERE BatchId=\"{batch_id}\";"
                logger.info(f"[GetTraineeInBatch] SQL Command: {command}")
                qs = cursor.execute(command)
                rows = cursor.fetchall()
                cols = [col[0] for col in cursor.description]
                result = [dict(zip(cols, row)) for row in rows]
                cursor.close
                logger.info(f"[GetTraineeInBatch] SQL Result: {result}")

            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                logger.error(f"GetTraineeInBatch {str(e)} at {str(exc_tb.tb_lineno)}")
                logger.info(f"[GetTraineeInBatch] SQL Result: {None}")
                return None
           
            if result != None:
                response['status_code'] = 200
                response['message'] = "Success"
                response['details'] = result
            else:
                response['status_code'] = 400
                response['message'] = "Bad request"
                response['details'] = result

            response['batch_id'] = str(batch_id)


        except Exception as e:  # noqa: F841
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("GetTraineeInBatch %s at %s",
                         str(e), str(exc_tb.tb_lineno))

        return Response(data=response)


GetTraineeInBatch = GetTraineeInBatch.as_view()

#208014





# class GetUserDetails(APIView):

#     authentication_classes = [SessionAuthentication, BasicAuthentication]

#     permission_classes = [IsAuthenticated]

#     def post(self, request, *args, **kwargs):

#         auth_header = request.META['HTTP_AUTHORIZATION']
#         import base64
#         encoded_credentials = auth_header.split(' ')[1]  # Removes "Basic " to isolate credentials
#         decoded_credentials = base64.b64decode(encoded_credentials).decode("utf-8").split(':')
#         username = decoded_credentials[0]
#         password = decoded_credentials[1]
#         print(username, password)

#         response = {"status_code": 500, "message": "Internal server error"}
#         try:

#             if username != settings.API_ACCESS_USERNAME:
#                 response['status_code'] = 400
#                 response['message'] = "Invalid Access"
#                 raise Exception("Invalid Access")

#             panelist_email_id = request.POST['panelist_email_id']
#             #panelist_password = request.POST['panelist_password']

#             try:
#                 #panelist_obj = authenticate(request, username=panelist_email_id, password=panelist_password)
#                 panelist_obj = "temp"
#                 if panelist_obj is not None:

#                     try:
#                         panelist_obj = Panelist.objects.get(username=panelist_email_id)

#                         response['groups'] = []

#                         if panelist_obj.role == "4":
#                             panelist_group_objs = GroupDiscussion.objects.filter(panelists__in=[panelist_obj])
#                             try:
#                                 group_search_text = request.POST['group_search_text']
#                                 if group_search_text is not None and group_search_text.strip() != "":
#                                     panelist_group_objs = panelist_group_objs.filter(group_name__icontains=group_search_text.strip())
#                             except:
#                                 pass
#                             try:
#                                 topic_search_text = request.POST['topic_search_text']
#                                 if topic_search_text is not None and topic_search_text.strip() != "":
#                                     panelist_group_objs = panelist_group_objs.filter(topic__topic_name__icontains=topic_search_text.strip())
#                             except:
#                                 pass

#                             try:
#                                 start_date = request.POST['start_date']
#                                 start_date = datetime.strptime(start_date, "%d/%m/%Y")
#                                 end_date = request.POST['end_date']
#                                 end_date = datetime.strptime(end_date, "%d/%m/%Y")
#                                 panelist_group_objs = panelist_group_objs.filter(gd_date__gte=start_date).filter(gd_date__lte=end_date)
#                             except:
#                                 panelist_group_objs = panelist_group_objs.filter(gd_date__gte=datetime.now().date())

#                             response['panlist_type'] = 2

#                             for group in panelist_group_objs:
#                                 group_dict = {
#                                     'group_name': group.group_name,
#                                     'group_topic': group.topic.topic_name,
#                                     'group_id': group.pk,
#                                     'gd_date_time': group.get_gd_time(),
#                                     'gd_duration': group.gd_duration
#                                 }

#                                 response['groups'].append(group_dict)
#                             response['status_code'] = 200
#                             response['message'] = "SUCCESS"
#                         elif panelist_obj.role == "5":

#                             panelist_group_objs = GroupDiscussion.objects.filter(hr_panelist=panelist_obj)

#                             try:
#                                 group_search_text = request.POST['group_search_text']
#                                 if group_search_text is not None and group_search_text.strip() != "":
#                                     panelist_group_objs = panelist_group_objs.filter(group_name__icontains=group_search_text.strip())
#                             except:
#                                 pass
#                             try:
#                                 topic_search_text = request.POST['topic_search_text']
#                                 if topic_search_text is not None and topic_search_text.strip() != "":
#                                     panelist_group_objs = panelist_group_objs.filter(topic__topic_name__icontains=topic_search_text.strip())
#                             except:
#                                 pass

#                             try:
#                                 start_date = request.POST['start_date']
#                                 start_date = datetime.strptime(start_date, "%d/%m/%Y")
#                                 end_date = request.POST['end_date']
#                                 end_date = datetime.strptime(end_date, "%d/%m/%Y")
#                                 panelist_group_objs = panelist_group_objs.filter(gd_date__gte=start_date).filter(gd_date__lte=end_date)
#                             except:
#                                 panelist_group_objs = panelist_group_objs.filter(gd_date__gte=datetime.now().date())

#                             response['panlist_type'] = 1

#                             for group in panelist_group_objs:
#                                 group_dict = {
#                                     'group_name': group.group_name,
#                                     'group_topic': group.topic.topic_name,
#                                     'group_id': group.pk,
#                                     'gd_date_time': group.get_gd_time(),
#                                     'gd_duration': group.gd_duration
#                                 }
#                                 response['groups'].append(group_dict)
#                             response['status_code'] = 200
#                             response['message'] = "SUCCESS"
#                         else:
#                             response['status_code'] = 302
#                             response['message'] = "User is not panelist"
#                     except Exception as e:
#                         exc_type, exc_obj, exc_tb = sys.exc_info()
#                         logger.error("GetGroupDiscussions %s at %s",
#                                      str(e), str(exc_tb.tb_lineno))
#                         response['status_code'] = 302
#                         response['message'] = "User is not panelist. details: " + str(e)
#                 else:
#                     response['status_code'] = 404
#                     response['message'] = "Panelist could not be authenticated"
#             except Exception as e:
#                 exc_type, exc_obj, exc_tb = sys.exc_info()
#                 logger.error("GetGroupDiscussions %s at %s",
#                              str(e), str(exc_tb.tb_lineno))
#         except Exception as e:  # noqa: F841
#             exc_type, exc_obj, exc_tb = sys.exc_info()
#             logger.error("GetGroupDiscussions %s at %s",
#                          str(e), str(exc_tb.tb_lineno))

#         return Response(data=response)


# GetUserDetailsAPI = GetUserDetails.as_view()





class GetCustomEnrolledTrainee(APIView):

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

        auth_header = request.META['HTTP_AUTHORIZATION']
        import base64
        encoded_credentials = auth_header.split(' ')[1]  # Removes "Basic " to isolate credentials
        decoded_credentials = base64.b64decode(encoded_credentials).decode("utf-8").split(':')
        username = decoded_credentials[0]
        password = decoded_credentials[1]

        response = {
            "status_code": 500,
            "message": "Internal server error"
            }
        try:
            if username != settings.API_ACCESS_USERNAME:
                response['status_code'] = 400
                response['message'] = "Invalid Access"
                raise Exception("Invalid Access")

            isa_id = request.data['isa_id']
            try:
                isa_id = request.data['isa_id']
                    
            except Exception as e:
                isa_id = None

            from_batch_end_date = request.data['from_batch_end_date']
            try:
                from_batch_end_date = request.data['from_batch_end_date']
                    
            except Exception as e:
                from_batch_end_date = None

            to_batch_end_date = request.data['to_batch_end_date']
            try:
                to_batch_end_date = request.data['to_batch_end_date']
                    
            except Exception as e:
                to_batch_end_date = None        

            logger.info(f"[GetCustomEnrolledTrainee] isa_id - Received - {isa_id}")

            if isa_id and from_batch_end_date and to_batch_end_date:
                print("good to go")
            else:
                raise Exception("Incomplete/wrong values in input parameter")    

            try:
                from django.db import connections
                cursor = connections['icici'].cursor()
                command = f"""
                select l7_enrldtraineeapplication.TraineeId, l7_enrldtraineeapplication.TraineeName,
                l7_enrldtraineeapplication.BatchId, l7_enrldtraineeapplication.ISACourseId, l7_enrldtraineeapplication.Course,
                batchcalendar.BatchStartDate, batchcalendar.BatchEndDate
                from
                l7_enrldtraineeapplication
                inner join batchcalendar
                on
                l7_enrldtraineeapplication.BatchId=batchcalendar.BatchId
                where l7_enrldtraineeapplication.ISACourseId like '{isa_id.zfill(3)}%' and
                batchcalendar.BatchEndDate >= \'{from_batch_end_date}\' and batchcalendar.BatchEndDate <= \'{to_batch_end_date}\';
                """
                logger.info(f"[GetCustomEnrolledTrainee] SQL Command: {command}")
                qs = cursor.execute(command)
                rows = cursor.fetchall()
                cols = [col[0] for col in cursor.description]
                result = [dict(zip(cols, row)) for row in rows]
                cursor.close
                logger.info(f"[GetCustomEnrolledTrainee] SQL Result: {result}")

            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                logger.error(f"GetCustomEnrolledTrainee {str(e)} at {str(exc_tb.tb_lineno)}")
                logger.info(f"[GetCustomEnrolledTrainee] SQL Result: {None}")
                return None
            
            if result != None:
                response['status_code'] = 200
                response['message'] = "Success"
                response['details'] = result
            else:
                response['status_code'] = 400
                response['message'] = "Bad request"
                response['details'] = result

            response['isa_id'] = str(isa_id)


        except Exception as e:  # noqa: F841
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("GetCustomEnrolledTrainee %s at %s",
                         str(e), str(exc_tb.tb_lineno))

        return Response(data=response)


GetCustomEnrolledTrainee = GetCustomEnrolledTrainee.as_view()



class GetUpcomingBatchList(APIView):

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

        auth_header = request.META['HTTP_AUTHORIZATION']
        import base64
        encoded_credentials = auth_header.split(' ')[1]  # Removes "Basic " to isolate credentials
        decoded_credentials = base64.b64decode(encoded_credentials).decode("utf-8").split(':')
        username = decoded_credentials[0]
        password = decoded_credentials[1]

        response = {
            "status_code": 500,
            "message": "Internal server error"
            }
        try:
            if username != settings.API_ACCESS_USERNAME:
                response['status_code'] = 400
                response['message'] = "Invalid Access"
                raise Exception("Invalid Access")

            try:
                isa_id = request.data['isa_id']
            except Exception as e:
                isa_id = None

            try:
                course_id = request.data['course_id']
            except Exception as e:
                course_id = None 

            try:
                batch_start_from_date = request.data['batch_start_from_date']
            except Exception as e:
                batch_start_from_date = None 

            try:
                batch_start_to_date = request.data['batch_start_to_date']
            except Exception as e:
                batch_start_to_date = None  

            if isa_id and course_id and batch_start_from_date and batch_start_to_date:
                print(f"good to go")
            else:
                raise Exception("Invalid values in the request parameter(s).")    

            try:
                from django.db import connections
                cursor = connections['icici'].cursor()
                
                command = f"""SELECT * FROM batchcalendar WHERE ISAId=\"{isa_id}\" and CourseId=\"{course_id}\" 
                and BatchStartDate >= \"{batch_start_from_date}\" and BatchStartDate <= \"{batch_start_to_date}\";
                """
                logger.info(f"[GetUpcomingBatchList] SQL Command: {command}")
                qs = cursor.execute(command)
                rows = cursor.fetchall()
                cols = [col[0] for col in cursor.description]
                result = [dict(zip(cols, row)) for row in rows]
                cursor.close
                logger.info(f"[GetUpcomingBatchList] SQL Result: {result}")

            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                logger.error(f"GetUpcomingBatchList {str(e)} at {str(exc_tb.tb_lineno)}")
                logger.info(f"[GetUpcomingBatchList] SQL Result: {None}")
                return None
            
            if result != None:
                response['status_code'] = 200
                response['message'] = "Success"
                response['details'] = result
            else:
                response['status_code'] = 400
                response['message'] = "Bad request"
                response['details'] = result

            response['isa_id'] = str(isa_id)


        except Exception as e:  # noqa: F841
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("GetUpcomingBatchList %s at %s",
                         str(e), str(exc_tb.tb_lineno))

        return Response(data=response)


GetUpcomingBatchList = GetUpcomingBatchList.as_view()




