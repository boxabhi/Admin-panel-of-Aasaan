


from console.utils_api import fetch_trainee_details_from_db,fetch_enrolled_trainee_details_from_db
from console.utils import send_sms  , send_custom_mail
from .models import *
from django.conf import settings

import os
import sys
import logging

from .thread import *

logging.basicConfig()
logger = logging.getLogger(__name__)




def send_sms_and_email_follow(follow_report=None , user=None):
    follow_objs = []
    if follow_objs is None:
        follow_objs = FollowUps.objects.filter(sms_status=False)
    else:
        follow_objs = FollowUps.objects.filter(follow_up_report = follow_report, sms_status = False)

  
    subject = "ICICI Foundation - Sourcing"
    message = f"""Dear , Welcome to ICICI Academy for Skill. Please click on the link to fill in the details in the admission enquiry form.  <Link> [non otp message]"""
    email_message = f"""<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <title>ICICI Foundation</title>
    <style type="text/css" media="screen">
    </style>
    </head>
    <body>
    <div style="padding:1em;border:0.1em black solid;" class="container">
    <p> Dear ,</p><p>
    Welcome to ICICI Academy for Skill. Please click on the link to fill in the details in the admission enquiry form. [Link]
    </p><p>Kindly connect with us incase of any issue.</p>
    <p>&nbsp;</p>
    <p>Regards,</p>
    <p>ICICI Foundation for Inclusive Growth</p></div></body>"""
    try:
        EmailAndSmsThread(follow_objs,subject ,email_message , message).start()

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.error(f"send_sms_and_email_follow {str(e)} at {str(exc_tb.tb_lineno)}")


def send_sms_and_email_sourcing(source_report = None , user = None):
    sourcing_objs = []
    if source_report is None:
        sourcing_objs = Sourcing.objects.filter(sms_status=False)
    else:
        sourcing_objs = Sourcing.objects.filter(sourcing_report=source_report, sms_status = False)


    subject = "ICICI Foundation - Sourcing"
    message = f"""Dear , Welcome to ICICI Academy for Skill. Please click on the link to fill in the details in the admission enquiry form.  <Link> [non otp message]"""
    email_message = f"""<head>
                    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
                    <title>ICICI Foundation</title>
                    <style type="text/css" media="screen">
                    </style>
                    </head>
                    <body>
                    <div style="padding:1em;border:0.1em black solid;" class="container">
                        <p>
                           Dear  ,
                        </p>
                        <p>
                          Welcome to ICICI Academy for Skill. Please click on the link to fill in the details in the admission enquiry form. [Link]
                        </p>
                        <p>Kindly connect with us incase of any issue.</p>
                        <p>&nbsp;</p>
                        <p>Regards,</p>
                        <p>ICICI Foundation for Inclusive Growth</p>
                    </div>
                    </body>"""

    try:
        EmailAndSmsThread(sourcing_objs,subject ,email_message , message).start()
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.error(f"send_sms_and_email_sourcing {str(e)} at {str(exc_tb.tb_lineno)}")


def send_sms_and_email_enrollment(enrollment_report =None , user = None):
    enrollment_objs = []
    if enrollment_report is None:
        enrollment_objs = Enrollments.objects.filter(sms_status=False)
    else:
        enrollment_objs = Enrollments.objects.filter(enrollment_report=enrollment_report , sms_status = False)


    subject = "ICICI Foundation - Sourcing"
    message = f"""Dear  Welcome to ICICI Academy for Skill. Please click on the link to fill in the details in the admission enquiry form.  <Link> [non otp message]"""
    email_message = f"""<head>
                    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
                    <title>ICICI Foundation</title>
                    <style type="text/css" media="screen">
                    </style>
                    </head>
                    <body>
                    <div style="padding:1em;border:0.1em black solid;" class="container">
                        <p>
                           Dear , 
                        </p>
                        <p>
                          Welcome to ICICI Academy for Skill. Please click on the link to fill in the details in the admission enquiry form. [Link]
                        </p>
                        <p>Kindly connect with us incase of any issue.</p>
                        <p>&nbsp;</p>
                        <p>Regards,</p>
                        <p>ICICI Foundation for Inclusive Growth</p>
                    </div>
                    </body>"""

    try:
        EmailAndSmsThread(enrollment_objs,subject ,email_message , message).start()
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.error(f"send_sms_and_email_enrollment {str(e)} at {str(exc_tb.tb_lineno)}")



def fetch_applicant_id(sourcing_report = None , user = None):
    sourcing_objs = []
    if user is None:
        sourcing_objs = Sourcing.objects.filter(application_id__isnull=True)
    else:
        sourcing_objs = Sourcing.objects.filter(sourcing_report = sourcing_report )

    print(sourcing_objs)
    try:
        for sourcing_obj in sourcing_objs:
            
            details = fetch_trainee_details_from_db(mobile_number=sourcing_obj.contact_no)
            applicant_ids = ''
            for detail in details:
                applicant_ids += str(detail.get('ApplicationId')) + ","

            if len(applicant_ids):
                sourcing_obj.application_id = applicant_ids.split(',')
                sourcing_obj.save()

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.error(f"fetch_applicant_id {str(e)} at {str(exc_tb.tb_lineno)}")





def fetch_follow_up_data(follow_up_report = None , user = None):
    follow_up_objs = []
    if follow_up_report:
        follow_up_objs = FollowUps.objects.filter(follow_up_report = follow_up_report)
    elif user:
        follow_up_objs = FollowUps.objects.filter(user = user)
    else:
        follow_up_objs = FollowUps.objects.all()

    try:
        for follow_up_obj in follow_up_objs:
            details = fetch_enrolled_trainee_details_from_db(trainee_id = follow_up_obj.trainee_id)
            details = details[0]

            follow_up_obj.contact_no = details.get('PhoneNo')
            follow_up_obj.email = details.get('Email')
            follow_up_obj.save()
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.error(f"fetch_follow_up_data {str(e)} at {str(exc_tb.tb_lineno)}")






def fetch_enrollment_data(enrollment_report =None , user=None):
    enrollment_objs = []
    if enrollment_report:
        enrollment_objs = Enrollments.objects.filter(enrollment_report = enrollment_report)
    elif user:
        enrollment_objs = Enrollments.objects.filter(user = user)
    else:
        enrollment_objs = Enrollments.objects.all()

    try:
        for enrollment_obj in enrollment_objs:
            details = fetch_enrolled_trainee_details_from_db(applicantion_id = enrollment_obj.applicant_id)
            details = details[0]
            enrollment_obj.contact_no = details.get('PhoneNo')
            enrollment_obj.trainee_id = details.get('TraineeId')
            print(details.get('TraineeId'))
            print(enrollment_obj.trainee_id)


            enrollment_obj.save()
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.error(f"fetch_enrollment_data {str(e)} at {str(exc_tb.tb_lineno)}")
                                     





