


from logging import error
import re 
import xlrd
from .models import *
from accounts.models import *

import os
import sys
import logging

logging.basicConfig()
logger = logging.getLogger(__name__)

from .thread import *

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from home.models import *

def get_value_or_na(input):
    if input is None:
        return "N/A"
    return input


def saveFile(uploaded_file):
    file_content = ContentFile(uploaded_file.read())
    file_path = default_storage.save(uploaded_file.name, file_content)
    print(file_path)
    return file_path


def check_full_name(full_name):
    if full_name.replace(" ", "").isalpha():
        return True
    else:
        return False

def check_contact_no(contact_no):
    Pattern = re.compile("(0/91)?[7-9][0-9]{9}") 
    return Pattern.match(contact_no) 
  

def check_email_id(email_id):
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if(re.search(regex,email_id)):  
        return True
    else:  
        return False 

def check_trainee_id(trainee_id):
    print(trainee_id)
    if len(trainee_id) <= 10 or len(trainee_id) > 12:
        return False
    if trainee_id.isdigit(): 
        return True
    return False

def check_applicant_id(applicant_id):
    if len(applicant_id) != 10 :
        return False
    if applicant_id.isdigit(): 
        return True
    return False


def refresh_enrollment_objs(objs):
    try:
        for obj in objs:
            details = fetch_enrolled_trainee_details_from_db(applicantion_id = obj.applicant_id)
            details = details[0]
            obj.contact_no = details.get('PhoneNo')
            obj.trainee_id = details.get('TraineeId')
            obj.save()
        return True
    except Exception as e:
        print(e)
    return False

def refresh_sourcing_objs(objs):
    try:
        for obj in objs:
          
            details = fetch_trainee_details_from_db(mobile_number=obj.contact_no)
            applicant_ids = []

            for detail in details:
                applicant = {}
                
                applicant['id'] = detail.get('ApplicationId')
                applicant['dob'] = str(detail.get('DateOfBirth'))
                applicant['email'] = detail.get('Email')
                applicant_ids.append(applicant)

            if len(applicant_ids):
                obj.application_id = json.dumps(applicant_ids)
                obj.save()
        
        return True

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.error(f"refresh_sourcing_objs {str(e)} at {str(exc_tb.tb_lineno)}")

    return False

def refresh_followups_objs(objs):

    try:
        for obj in objs:
            print('!!!!!')
            print(obj)
            print('!!!!!')

            details = fetch_enrolled_trainee_details_from_db(trainee_id = obj.trainee_id)
            details = details[0]
            obj.contact_no = details.get('PhoneNo')
            obj.email = details.get('Email')
            obj.save()
        return True
    except Exception as e:
        print(e)
    return False


def refresh_objs(objs , option):


    if option == 1:
        return refresh_enrollment_objs(objs)
    elif option == 2:
        return refresh_sourcing_objs(objs)
    elif option == 3:
        return refresh_followups_objs(objs)

    


def send_sms_and_email_to_objs(objs):
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
        EmailAndSmsThread(objs,subject ,email_message , message).start()
        return True
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.error(f"send_sms_and_email_sourcing {str(e)} at {str(exc_tb.tb_lineno)}")
        return False


import json
def check_source_from_excel(file_path,user):
    try:
        wb = xlrd.open_workbook(file_path)
        sheet = wb.sheet_by_index(0)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.error(f"import_source_from_excel {str(e)} at {str(exc_tb.tb_lineno)}")
        return False, "Excel File Read Error"

    errors = []
    count = 0
    try:
        rows = sheet.nrows - 1
        
        for i in range(rows):
            count += 1
            full_name = str(sheet.cell_value(i+1,1)).strip()
            contact_no = str(sheet.cell_value(i+1,2)).strip()
            email_id = str(sheet.cell_value(i+1,3)).strip()
            centre_name = str(sheet.cell_value(i+1,4)).strip()
            faculty_name = str(sheet.cell_value(i+1,5)).strip()


            if not check_full_name(full_name):
                #errors.append("not a valid full name at " +str(i+1))
                errors.append(f'Row {i+1} : Invalid Name - Name should not contain special characters or digits')


            if not check_contact_no(contact_no):
                errors.append(f'Row {i+1} : Invalid Mobile No - Cannot have alphabets / should be of 10 digits etc.')

                #errors.append("not a vald contact number at "+ str(i+1))

            if not check_email_id(email_id):
                errors.append(f'Row {i+1} : Invalid Email - Not in proper format.')

                #errors.append("not a valid email id at " + str(i+1))

        errors_len = len(errors)
        if len(errors):
            errors = json.dumps(errors)
        SourcingReportStatus.objects.create(user=user ,file_path=file_path,total_errors=errors_len,errors_desc=errors , total_entries= count,current_status=1)
        
    except Exception as e:
        print(e)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.error(f"NearestAcademy {str(e)} at {str(exc_tb.tb_lineno)}")

    print(errors)
    if len(errors) == 0:
        return errors,True        
    return errors , False


def import_source_from_excel(file_path , user ,sourcing_report):
    try:
        wb = xlrd.open_workbook(file_path)
        sheet = wb.sheet_by_index(0)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.error(f"import_source_from_excel {str(e)} at {str(exc_tb.tb_lineno)}")
        return False, "Excel File Read Error"

    rows = sheet.nrows - 1
    excel_data = []
    for i in range(rows):
        full_name = str(sheet.cell_value(i+1,1)).strip()
        contact_no = str(sheet.cell_value(i+1,2))[0:-2]
        email_id = str(sheet.cell_value(i+1,3)).strip()
        centre_name = str(sheet.cell_value(i+1,4)).strip()
        faculty_name = str(sheet.cell_value(i+1,5)).strip()


        Sourcing.objects.create(sourcing_report =sourcing_report ,uploaded_by = user ,full_name=full_name , contact_no=contact_no , email=email_id , centre_name =centre_name , faculty_name=faculty_name)

    return True







def check_follow_ups_from_excel(file_path , user):
    try:
        wb = xlrd.open_workbook(file_path)
        sheet = wb.sheet_by_index(0)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.error(f"follow_ups_from_excel {str(e)} at {str(exc_tb.tb_lineno)}")
        return False, "Excel File Read Error"

    errors = []
    count = 0
    try:
        rows = sheet.nrows - 1
        
        for i in range(rows):
            count += 1
            trainee_id = str(sheet.cell_value(i+1,1)).strip()[:-2]
            centre_name = str(sheet.cell_value(i+1,2)).strip()
            faculty_name = str(sheet.cell_value(i+1,3)).strip()

            print(trainee_id)
            if not check_trainee_id(trainee_id):
                errors.append(f'Row {i+1} : invalid trainee id. Must be 11 digit numeric value')
                #errors.append("not a valid trainee id  at " +str(i+1))


           

        errors_len = len(errors)
        if len(errors):
            errors = json.dumps(errors)
        FollowUpsReportStatus.objects.create(user=user ,file_path=file_path,total_errors=errors_len,errors_desc=errors , total_entries= count,current_status=1)
        
    except Exception as e:
        print(e)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.error(f"check_follow_ups_from_excel {str(e)} at {str(exc_tb.tb_lineno)}")

    print(errors)
    if len(errors) == 0:
        return errors,True        
    return errors , False


def check_enrollment_from_excel(file_path  , user):
    try:
        wb = xlrd.open_workbook(file_path)
        sheet = wb.sheet_by_index(0)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.error(f"follow_ups_from_excel {str(e)} at {str(exc_tb.tb_lineno)}")
        return False, "Excel File Read Error"

    errors = []
    count = 0
    try:
        rows = sheet.nrows - 1
        
        for i in range(rows):
            count += 1
            applicant_id = str(sheet.cell_value(i+1,1)).strip()[:-2]
            print(str(sheet.cell_value(i+1,1)).strip())
            print(len(str(sheet.cell_value(i+1,1)).strip()))
            if not check_applicant_id(applicant_id):
                errors.append(f'Row {i+1} : invalid applicant id. Must be 11 digit numeric value ')
        errors_len = len(errors)
        if len(errors):
            errors = json.dumps(errors)
        EnrollmentReportStatus.objects.create(user=user ,file_path=file_path,total_errors=errors_len,errors_desc=errors , total_entries= count,current_status=1)
        
    except Exception as e:
        print(e)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.error(f"check_follow_ups_from_excel {str(e)} at {str(exc_tb.tb_lineno)}")

    if len(errors) == 0:
        return errors,True        
    return errors , False



def import_enrollments_from_excel(file_path , user ,enrollment_report):
    try:
        wb = xlrd.open_workbook(file_path)
        sheet = wb.sheet_by_index(0)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.error(f"import_source_from_excel {str(e)} at {str(exc_tb.tb_lineno)}")
        return False, "Excel File Read Error"

    rows = sheet.nrows - 1
    excel_data = []
    for i in range(rows):
        applicant_id = str(sheet.cell_value(i+1,1)).strip()[:-2]
        Enrollments.objects.create(enrollment_report =enrollment_report  ,applicant_id=applicant_id )

    return True


def import_follow_ups_from_excel(file_path , user ,follow_up_report):
    try:
        wb = xlrd.open_workbook(file_path)
        sheet = wb.sheet_by_index(0)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.error(f"import_source_from_excel {str(e)} at {str(exc_tb.tb_lineno)}")
        return [False], False

    rows = sheet.nrows - 1
    excel_data = []
    for i in range(rows):
        trainee_id = str(sheet.cell_value(i+1,1)).strip()[:-2]
        centre_name = str(sheet.cell_value(i+1,2)).strip()
        faculty_name = str(sheet.cell_value(i+1,3)).strip()
        FollowUps.objects.create(follow_up_report =follow_up_report  ,trainee_id=trainee_id , centre_name =centre_name , faculty_name=faculty_name)

    return True


def import_users(file_path):
    ImportUsersFromExcel(file_path).start()
    return True
    # try:
    #     wb = xlrd.open_workbook(file_path)
    #     sheet = wb.sheet_by_index(0)
    # except Exception as e:
    #     exc_type, exc_obj, exc_tb = sys.exc_info()
    #     logger.error(f"import_source_from_excel {str(e)} at {str(exc_tb.tb_lineno)}")
    #     return [False], False

        
    # rows = sheet.nrows - 1
    # for i in range(rows):
    #     email_id = str(sheet.cell_value(i+1,1)).strip()
    #     emp_id = str(sheet.cell_value(i+1,2))
    #     first_name = str(sheet.cell_value(i+1,3)).strip()
    #     last_name = str(sheet.cell_value(i+1,4)).strip()
    #     raw_permissions = str(sheet.cell_value(i+1,4)).strip()

    #     profile_obj = Profile.objects.create(username = email_id , email = email_id  , first_name = first_name  , last_name = last_name)
    #     profile_obj.set_password(f'ICICI@{email_id}')
        
    #     permissions = raw_permissions.split(',')

    #     for permission in permissions:
    #         role_obj = Role.objects.filter(role_name = permission).first()
    #         if role_obj:
    #             profile_obj.role.add(role_obj)

    #     profile_obj.save()
        
    return True





        #FollowUps.objects.create(follow_up_report =follow_up_report  ,trainee_id=trainee_id , centre_name =centre_name , faculty_name=faculty_name)

def export_roles(role_objs):
    from xlwt import Workbook, easyxf
    export_nps_wb = Workbook()
    sheet_name = "Applicant Profiles"

    sheet1 = export_nps_wb.add_sheet(
        sheet_name, cell_overwrite_ok=True)
    st = easyxf("align: horiz center; font: bold on")
    i = 0
    sheet1.write(0, i, "Role name", st)
    i += 1
    sheet1.write(0, i, "Role Sign", st)
    i += 1
    
    
    row = 1
    for role in role_objs:
        print(role.role_name)
        try:
            i = 0
            sheet1.write(row, i, get_value_or_na(role.role_name))
            i += 1
            sheet1.write(row, i, get_value_or_na(role.pk))
            i +=1
            row += 1
        except Exception as e:
            print(logger.error(f"check_users_from_excel {str(e)} at {str(exc_tb.tb_lineno)}"))
            
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error(f"check_users_from_excel {str(e)} at {str(exc_tb.tb_lineno)}")


    export_nps_wb.save(str(settings.MEDIA_ROOT) + '/roles.xls')
    file_path =  str('roles.xls')

    return file_path , True
           

def check_impact_box_upload(file_path):
    try:
        wb = xlrd.open_workbook(file_path)
        sheet = wb.sheet_by_index(0)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.error(f"check_impact_box_upload {str(e)} at {str(exc_tb.tb_lineno)}")
        return [], False
    
    errors = []
    count = 0
    try:
        rows = sheet.nrows - 1
        for i in range(rows):
            count += 1
            total = str(sheet.cell_value(i+1,1))
            total_males = str(sheet.cell_value(i+1,2))
            total_females = str(sheet.cell_value(i+1,3))
            total_this_month = str(sheet.cell_value(i+1,4))
            total_males_ = str(sheet.cell_value(i+1,5))
            total_females_ = str(sheet.cell_value(i+1,6))
            this_fy_total = str(sheet.cell_value(i+1,7))
            this_fy_males = str(sheet.cell_value(i+1,8))
            this_fy_females = str(sheet.cell_value(i+1,9))

    except Exception as e:
        print(e)

    ImpactBoxUpload.objects.create(
        file_path = file_path,
        total_entries = count   
    )
    

def import_internal_job_posting(file_path):
    try:
        wb = xlrd.open_workbook(file_path)
        sheet = wb.sheet_by_index(0)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.error(f"import_internal_job_posting {str(e)} at {str(exc_tb.tb_lineno)}")
        return [], False
    errors = []
    count = 0
    try:
        rows = sheet.nrows - 1
        for i in range(rows):
            count += 1
            position = str(sheet.cell_value(i+1,1))
            location = str(sheet.cell_value(i+1,2))
            job_description = str(sheet.cell_value(i+1,3))

            InternalJobPosting.objects.create(
                position   = position,
                location   = location,
                job_description   = job_description,
            )

    except Exception as e:
        return False

    
    return True




def import_impact_box(file_path):
    try:
        wb = xlrd.open_workbook(file_path)
        sheet = wb.sheet_by_index(0)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.error(f"check_impact_box_upload {str(e)} at {str(exc_tb.tb_lineno)}")
        return [], False
    
    count = 1
    try:
        impact_obj = ImpactBox.objects.all()
        impact_obj.delete()
        impact_obj = ImpactBox.objects.create()
        rows = sheet.nrows - 1
        for i in range(rows):
            total = str(sheet.cell_value(i+1,1))
            total_males = str(sheet.cell_value(i+1,2))
            total_females = str(sheet.cell_value(i+1,3))
            total_this_month = str(sheet.cell_value(i+1,4))
            total_males_ = str(sheet.cell_value(i+1,5))
            total_females_ = str(sheet.cell_value(i+1,6))
            this_fy_total = str(sheet.cell_value(i+1,7))
            this_fy_males = str(sheet.cell_value(i+1,8))
            this_fy_females = str(sheet.cell_value(i+1,9))

            if count == 1:
                isa_total  = total
                isa_total_males  = total_males
                isa_total_females  = total_females

                isa_this_month_total  = total_this_month
                isa_males  =total_males_
                isa_females  = total_females_
                isa_this_fy_total  = this_fy_total
                isa_this_fv_males  = this_fy_males
                isa_this_fv_females  =this_fy_females

                
                impact_obj.isa_total  = isa_total[0]
                impact_obj.isa_total_males  = isa_total_males[0]
                impact_obj.isa_total_females  = isa_total_females[0]
                impact_obj.isa_this_month_total  = isa_this_month_total[0]
                impact_obj.isa_males  = isa_males[0]
                impact_obj.isa_females  = isa_females[0]
                impact_obj.isa_this_fy_total  = isa_this_fy_total[0]
                impact_obj.isa_this_fv_males  = isa_this_fv_males[0]
                impact_obj.isa_this_fv_females  = isa_this_fv_females[0]

                impact_obj.save()
            
            elif count == 2:
                rl_total =     total
                rl_total_males =     total_males
                rl_total_females =     total_females
                rl_this_month_total =     total_this_month
                rl_males =     total_males_
                rl_females =     total_females_
                rl_this_fy_total =     this_fy_total
                rl_this_fv_males =     this_fy_males
                rl_this_fv_females =     this_fy_females

                impact_obj.rl_total   = rl_total[0]
                impact_obj.rl_total_males  = rl_total_males[0]
                impact_obj.rl_total_females  = rl_total_females[0]
                impact_obj.rl_this_month_total  = rl_this_month_total[0]
                impact_obj.rl_males  = rl_males[0]
                impact_obj.rl_females  = rl_females[0]
                impact_obj.rl_this_fy_total  = rl_this_fy_total[0]
                impact_obj.rl_this_fv_males  = rl_this_fv_males[0]
                impact_obj.rl_this_fv_females  = rl_this_fv_females[0]

                impact_obj.save()


            
            elif count == 3:
                rseti_total =        total
                rseti_total_males =        total_males
                rseti_total_males =        total_females
                rseti_this_month_total =        total_this_month
                rseti_males =        total_males_
                rseti_females =        total_females_
                rseti_this_fy_total =        this_fy_total
                rseti_this_fv_males =        this_fy_males
                rseti_this_fv_females =        this_fy_females


                impact_obj.rseti_total = total[0]
                impact_obj.rseti_total_males = total_males[0]
                impact_obj.rseti_total_females = total_females[0]
                impact_obj.rseti_this_month_total = total_this_month[0]
                impact_obj.rseti_males = total_males_[0]
                impact_obj.rseti_females = total_females_[0]
                impact_obj.rseti_this_fy_total = this_fy_total[0]
                impact_obj.rseti_this_fv_males = this_fy_males[0]
                impact_obj.rseti_this_fv_females = this_fy_females[0]

                impact_obj.save()

            count += 1

    except Exception as e:
        print(e)


def check_users_from_excel(file_path , file_name):
    print(file_path)
    try:
        wb = xlrd.open_workbook(file_path)
        sheet = wb.sheet_by_index(0)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.error(f"check_users_from_excel {str(e)} at {str(exc_tb.tb_lineno)}")
        return [], False

    errors = []
    count = 0
    try:
        rows = sheet.nrows - 1
        
        for i in range(rows):
            count += 1
            email_id = str(sheet.cell_value(i+1,1))
            emp_id = str(sheet.cell_value(i+1,2))
            first_name = sheet.cell_value(i+1 , 3)
            last_name = sheet.cell_value(i+1 , 4)
            is_admin = str(sheet.cell_value(i+1,3))
        

            if  Profile.objects.filter(email = email_id).first():
                errors.append(f'Row {i+1} : users exists with email id {email_id} ')
            
            if  Profile.objects.filter(emp_id = emp_id).first():
                errors.append(f'Row {i+1} : users exists with emp id {emp_id} ')
             
        
        errors_len = len(errors)
        if len(errors):
            errors = json.dumps(errors)
        UserUploadExcel.objects.create(file_path=file_name,total_errors=errors_len,errors_desc=errors , total_entries= count)
        
    except Exception as e:
        print(e)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.error(f"check_users_from_excel {str(e)} at {str(exc_tb.tb_lineno)}")

    if len(errors) == 0:
        return errors,True        
    return errors , False



def export_users_excel(user_objs):
    
    from xlwt import Workbook, easyxf
    export_nps_wb = Workbook()
    sheet_name = "User Profiles"

    sheet1 = export_nps_wb.add_sheet(
        sheet_name, cell_overwrite_ok=True)
    st = easyxf("align: horiz center; font: bold on")
    i = 0
    sheet1.write(0, i, "User email", st)
    i += 1
    sheet1.write(0, i, "Emp id", st)
    i += 1
    sheet1.write(0, i, "First name", st)
    i += 1
    sheet1.write(0, i, "Last name", st)
    i += 1
    sheet1.write(0, i, "Is admin", st)
    i += 1
    sheet1.write(0, i, "Permission", st)
    i += 1
    sheet1.write(0, i, "Is active", st)
    i += 1
    
    sheet1.write(0, i, "Created on", st)
    i += 1
    sheet1.write(0, i, "Updated on", st)
    i += 1
    
    row = 1
    for user_obj in user_objs:
        try:
            i = 0
            sheet1.write(row, i, get_value_or_na(user_obj.email))
            i += 1
            sheet1.write(row, i, get_value_or_na(user_obj.emp_id))
            i += 1
            sheet1.write(row, i, get_value_or_na(user_obj.first_name))
            i += 1
            sheet1.write(row, i, get_value_or_na(user_obj.last_name))
            i += 1
            is_admin = 'No - (manager)'
            if len(roles_objs) == len(user_obj.role.all()):
                is_admin = 'Yes - (admin)'
            sheet1.write(row, i, is_admin)
            i += 1 
            
            roles = ''
            roles_objs = Role.objects.all()
            
            for role in user_obj.role.all():
                print(role)
                roles += role.role_name + ','
            
            print(len(roles))
            
            if len(roles) == 0 :
                roles = "No role assigned"
            
            
            
            sheet1.write(row, i, str(roles))
            i += 1
            #print(user_obj.created_at.strftime("%d/%m/%Y %I:%M %p"))
                
            sheet1.write(row, i, get_value_or_na(user_obj.is_active))
            i += 1 
           

            sheet1.write(row, i, get_value_or_na(user_obj.created_at.strftime("%d/%m/%Y %I:%M %p")))
            
            i += 1
            sheet1.write(row, i, get_value_or_na(user_obj.updated_at.strftime("%d/%m/%Y %I:%M %p")))
            i += 1   
            
            row += 1
        except Exception as e:
            
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(logger.error(f"check_users_from_excel {str(e)} at {str(exc_tb.tb_lineno)}"))
            
            logger.error(f"check_users_from_excel {str(e)} at {str(exc_tb.tb_lineno)}")


    export_nps_wb.save(str(settings.MEDIA_ROOT) + '/users.xls')
    file_path =  str('users.xls')
    print(file_path)
    return file_path , True




def export_referrals(referral):
    return
      
    from xlwt import Workbook, easyxf
    export_nps_wb = Workbook()
    sheet_name = "Referrals"

    sheet1 = export_nps_wb.add_sheet(
        sheet_name, cell_overwrite_ok=True)

    st = easyxf("align: horiz center; font: bold on")
    i = 0
    sheet1.write(0, i, "S.No", st)
    i += 1
    sheet1.write(0, i, 'Referrer name' , st)
    i +=1
    sheet1.write(0, i, 'Referrer mobile' , st)
    i +=1
    sheet1.write(0, i, 'referrer email' , st)
    i +=1
    sheet1.write(0, i, 'referee name' , st)
    i +=1
    sheet1.write(0, i, 'referee mobile' , st)
    i +=1
    sheet1.write(0, i, 'referee email' , st)
    i +=1
    sheet1.write(0, i, 'source' , st)
    i +=1
    sheet1.write(0, i, 'created at' , st)
    i +=1
    sheet1.write(0, i, 'updated at' , st)
    i +=1

    


def import_payment(file_path):
    ImportPaymentFromExcel(file_path).start()

    # try:
    #     wb = xlrd.open_workbook(file_path)
    #     sheet = wb.sheet_by_index(0)
    # except Exception as e:
    #     exc_type, exc_obj, exc_tb = sys.exc_info()
    #     logger.error(f"import_source_from_excel {str(e)} at {str(exc_tb.tb_lineno)}")
    #     return False, "Excel File Read Error"
    
    # payment_objs = PaymentSheet.objects.filter(is_deleted =False)

    # for payment_obj in payment_objs:
    #     payment_obj.is_deleted = True
    #     payment_obj.save()


    # rows = sheet.nrows - 1

    # excel_data = []
    # for i in range(rows):
        
    #     ClaimNo   = str(sheet.cell_value(i+1,1)).strip()
    #     IFIG_NO = str(sheet.cell_value(i+1,2)).strip()
    #     Inward = str(sheet.cell_value(i+1,3)).strip()
    #     Month = str(sheet.cell_value(i+1,4)).strip()
    #     Employee_Code = str(sheet.cell_value(i+1,5)).strip()
    #     Inwarded_By = str(sheet.cell_value(i+1,6)).strip()
    #     Vendor_Code = str(sheet.cell_value(i+1,7)).strip()
    #     Vendor_Name = str(sheet.cell_value(i+1,8)).strip()
    #     Mail_Received_From = str(sheet.cell_value(i+1,9)).strip()
    #     Do_Name_PM_Name = str(sheet.cell_value(i+1,10)).strip()
    #     Claim_Type = str(sheet.cell_value(i+1,11)).strip()
    #     From_Date = str(sheet.cell_value(i+1,12)).strip()
    #     To_Date = str(sheet.cell_value(i+1,13)).strip()
    #     Department = str(sheet.cell_value(i+1,14)).strip()
    #     PO_Number = str(sheet.cell_value(i+1,15)).strip()
    #     Invoice_No = str(sheet.cell_value(i+1,16)).strip()
    #     Invoice_Date = str(sheet.cell_value(i+1,17)).strip()
    #     Invoice_Amount = str(sheet.cell_value(i+1,18)).strip()
    #     Ramco     = str(sheet.cell_value(i+1,19)).strip()
    #     Entry_Date     = str(sheet.cell_value(i+1,20)).strip()
    #     Authorised_Date     = str(sheet.cell_value(i+1,21)).strip()
    #     Entry_Done_By     = str(sheet.cell_value(i+1,22)).strip()
    #     USER_ID = str(sheet.cell_value(i+1,23)).strip()
    #     Payment     = str(sheet.cell_value(i+1,24)).strip()
       
    #     Upload_Number     = str(sheet.cell_value(i+1,25)).strip()
    #     UTR_NO     = str(sheet.cell_value(i+1,26)).strip()
    #     Payment_Date     = str(sheet.cell_value(i+1,27)).strip()
    #     UPLOAD_STATUS     = str(sheet.cell_value(i+1,28)).strip()
    #     STATUS     = str(sheet.cell_value(i+1,29)).strip()
    #     Remarks     = str(sheet.cell_value(i+1,30)).strip()
    #     Received_Date     = str(sheet.cell_value(i+1,31)).strip()
    #     Objection     = str(sheet.cell_value(i+1,32)).strip()
    #     Objection_Raised_By     = str(sheet.cell_value(i+1,33)).strip()
    #     Query     = str(sheet.cell_value(i+1,34)).strip()
    #     Resolution_Date     = str(sheet.cell_value(i+1,35)).strip()
    #     Resolution_By     = str(sheet.cell_value(i+1,36)).strip()
    #     Rejection_Date     = str(sheet.cell_value(i+1,37)).strip()
    #     Rejection_Done_By     = str(sheet.cell_value(i+1,38)).strip()
    #     Location     = str(sheet.cell_value(i+1,39)).strip()
    #     Classification     = str(sheet.cell_value(i+1,40)).strip()
    #     Reporting_Mngr     = str(sheet.cell_value(i+1,41)).strip()
    #     Zonal_Head     = str(sheet.cell_value(i+1,42)).strip()
    #     Zone     = str(sheet.cell_value(i+1,43)).strip()
    #     Period     = str(sheet.cell_value(i+1,44)).strip()
    #     Age     = str(sheet.cell_value(i+1,45)).strip()
    #     HGS     = str(sheet.cell_value(i+1,46)).strip()
      


    #     PaymentSheet.objects.create(
    #             ClaimNo  =  ClaimNo,
    #             IFIG_NO  =  IFIG_NO,
    #             Inward  =  Inward,
    #             Month  =  Month,
    #             Employee_Code  =  Employee_Code,
    #             Inwarded_By  =  Inwarded_By,
    #             Vendor_Code  =  Vendor_Code,
    #             Vendor_Name  =  Vendor_Name,
    #             Mail_Received_From  =  Mail_Received_From,
    #             Do_Name_PM_Name  =  Do_Name_PM_Name,
    #             Claim_Type  =  Claim_Type,
    #             From_Date  =  From_Date,
    #             To_Date  =  To_Date,
    #             Department  =  Department,
    #             PO_Number  =  PO_Number,
    #             Invoice_No  =  Invoice_No,
    #             Invoice_Date  =  Invoice_Date,
    #             Invoice_Amount  =  Invoice_Amount,
    #             Ramco  =  Ramco,
                
    #             Entry_Date  =  Entry_Date,
    #             Authorised_Date  =  Authorised_Date,
    #             Entry_Done_By  =  Entry_Done_By,
    #             USER_ID  =  USER_ID,
    #             Payment  =  Payment,
               
    #             Upload_Number  =  Upload_Number,
    #             UTR_NO  =  UTR_NO,
    #             Payment_Date  =  Payment_Date,
    #             UPLOAD_STATUS  =  UPLOAD_STATUS,
    #             STATUS  =  STATUS,
                
    #             Remarks  =  Remarks,
    #             Received_Date  =  Received_Date,
    #             Objection  =  Objection,
    #             Objection_Raised_By  =  Objection_Raised_By,
    #             Query  =  Query,
               
    #             Resolution_Date  =  Resolution_Date,
    #             Resolution_By  =  Resolution_By,
    #             Rejection_Date  =  Rejection_Date,
    #             Rejection_Done_By  =  Rejection_Done_By,
    #             Location  =  Location,
    #             Classification  =  Classification,
    #             Reporting_Mngr  =  Reporting_Mngr,
    #             Zonal_Head  =  Zonal_Head,
    #             Zone  =  Zone,
    #             Period  =  Period,
    #             Age  =  Age,
    #             HGS  =  HGS,
                
    #     )


    return True

        