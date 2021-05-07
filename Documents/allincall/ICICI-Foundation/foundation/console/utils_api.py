
import sys
from datetime import datetime

import logging

logging.basicConfig()
logger = logging.getLogger(__name__)

def fetch_batch_details_from_db(batch_id):
    try:
        from django.db import connections
        cursor = connections['icici'].cursor()
        logger.info(f"[fetch_batch_details_from_db] Batch ID - RECEIVED - {batch_id}")
        #command = f"SELECT BatchId,BatchName,BatchStartDate,BatchStartDate FROM batchcalendar WHERE {batch_id}"
        command = f"SELECT * FROM batchcalendar WHERE BatchId={batch_id};"
        logger.info(f"[fetch_batch_details_from_db] SQL Command: {command}")
        qs = cursor.execute(command)
        rows = cursor.fetchall()
        cols = [col[0] for col in cursor.description]
        result = [dict(zip(cols, row)) for row in rows]
        cursor.close
        logger.info(f"[fetch_batch_details_from_db] SQL Result: {result}")
        return result

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.error(f"fetch_batch_details_from_db {str(e)} at {str(exc_tb.tb_lineno)}")
        logger.info(f"[fetch_batch_details_from_db] SQL Result: {None}")
        return None

def fetch_employee_details_from_db(employee_id):
    try:
        from django.db import connections
        cursor = connections['icici'].cursor()
        logger.info(f"[fetch_employee_details_from_db] Employee ID - RECEIVED - {employee_id}")
        command = f"SELECT * FROM masterstaff WHERE EmpId=\"{employee_id}\""
        logger.info(f"[fetch_employee_details_from_db] SQL Command: {command}")
        qs = cursor.execute(command)
        rows = cursor.fetchall()
        cols = [col[0] for col in cursor.description]
        result = [dict(zip(cols, row)) for row in rows]
        cursor.close
        logger.info(f"[fetch_employee_details_from_db] SQL Result: {result}")
        return result

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.error(f"fetch_employee_details_from_db {str(e)} at {str(exc_tb.tb_lineno)}")
        logger.info(f"[fetch_employee_details_from_db] SQL Result: {None}")
        return None


def fetch_skill_academy_from_db(isa_id):
    try:
        from django.db import connections
        cursor = connections['icici'].cursor()
        logger.info(f"[fetch_skill_academy_from_db] ISA ID - RECEIVED - {isa_id}")
        command = f"SELECT * FROM l4_skillacademies WHERE ISAId=\"{isa_id}\";"
        logger.info(f"[fetch_skill_academy_from_db] SQL Command: {command}")
        qs = cursor.execute(command)
        rows = cursor.fetchall()
        cols = [col[0] for col in cursor.description]
        result = [dict(zip(cols, row)) for row in rows]
        cursor.close
        logger.info(f"[fetch_skill_academy_from_db] SQL Result: {result}")
        return result

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.error(f"fetch_skill_academy_from_db {str(e)} at {str(exc_tb.tb_lineno)}")
        logger.info(f"[fetch_skill_academy_from_db] SQL Result: {None}")
        return None

def fetch_enrolled_trainee_details_from_db(trainee_id=None,applicantion_id=None):
    try:
        logger.info(f"[fetch_enrolled_trainee_details_from_db] Trainee ID - RECEIVED - {trainee_id}")
        logger.info(f"[fetch_enrolled_trainee_details_from_db] Application ID - RECEIVED - {applicantion_id}")
        from django.db import connections
        cursor = connections['icici'].cursor()
        if trainee_id:
            command = f"""
            SELECT l7_enrldtraineeapplication.*, l7_traineeapplications.PhoneNo, l7_traineeapplications.DateOfBirth,l7_traineeapplications.Email 
            FROM l7_enrldtraineeapplication 
            LEFT JOIN
            l7_traineeapplications
            ON
            l7_enrldtraineeapplication.ApplicationId = l7_traineeapplications.ApplicationId
            WHERE 
            l7_enrldtraineeapplication.TraineeId={trainee_id};
            """
        elif applicantion_id:
            command = f"""
            SELECT l7_enrldtraineeapplication.*, l7_traineeapplications.PhoneNo, l7_traineeapplications.DateOfBirth ,l7_traineeapplications.Email
            FROM l7_enrldtraineeapplication 
            LEFT JOIN
            l7_traineeapplications
            ON
            l7_enrldtraineeapplication.ApplicationId = l7_traineeapplications.ApplicationId
            WHERE 
            l7_enrldtraineeapplication.ApplicationId={applicantion_id};
            """
        else:
            raise Exception("Blank values in the parameters")
        logger.info(f"[fetch_enrolled_trainee_details_from_db] SQL Command: {command}")
        qs = cursor.execute(command)
        rows = cursor.fetchall()
        cols = [col[0] for col in cursor.description]
        result = [dict(zip(cols, row)) for row in rows]
        cursor.close
        logger.info(f"[fetch_enrolled_trainee_details_from_db] SQL Result: {result}")
        return result

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.error(f"fetch_enrolled_trainee_details_from_db {str(e)} at {str(exc_tb.tb_lineno)}")
        logger.info(f"[fetch_enrolled_trainee_details_from_db] SQL Result: {None}")
        return None


def fetch_trainee_details_from_db(mobile_number=None,dob=None,application_id=None):
    try:
        logger.info(f"[fetch_trainee_details_from_db] Mobile Number - RECEIVED - {mobile_number}")
        logger.info(f"[fetch_trainee_details_from_db] DoB - RECEIVED - {dob}")
        logger.info(f"[fetch_trainee_details_from_db] application_id - RECEIVED - {application_id}")
        
        from django.db import connections
        cursor = connections['icici'].cursor()
        
        if mobile_number and not dob:
            command = f"""
            SELECT l7_traineeapplications.*, l7_enrldtraineeapplication.TraineeId 
            FROM 
            l7_traineeapplications LEFT JOIN l7_enrldtraineeapplication
            ON
            l7_traineeapplications.ApplicationId = l7_enrldtraineeapplication.ApplicationId
            WHERE 
            l7_traineeapplications.PhoneNo={mobile_number};
            """
        elif not mobile_number and dob :
            command = f"""
            SELECT l7_traineeapplications.*, l7_enrldtraineeapplication.TraineeId 
            FROM 
            l7_traineeapplications LEFT JOIN l7_enrldtraineeapplication
            ON
            l7_traineeapplications.ApplicationId = l7_enrldtraineeapplication.ApplicationId
            WHERE 
            l7_traineeapplications.DateOfBirth="{dob}";
            """
        elif mobile_number and dob:
            command = f"""
            SELECT l7_traineeapplications.*, l7_enrldtraineeapplication.TraineeId 
            FROM 
            l7_traineeapplications LEFT JOIN l7_enrldtraineeapplication
            ON
            l7_traineeapplications.ApplicationId = l7_enrldtraineeapplication.ApplicationId
            WHERE 
            l7_traineeapplications.DateOfBirth="{dob}" AND l7_traineeapplications.PhoneNo={mobile_number};
            """
        elif application_id and not mobile_number and not dob:
            command = f"""
            SELECT l7_traineeapplications.*, l7_enrldtraineeapplication.TraineeId 
            FROM 
            l7_traineeapplications LEFT JOIN l7_enrldtraineeapplication
            ON
            l7_traineeapplications.ApplicationId = l7_enrldtraineeapplication.ApplicationId
            WHERE 
            l7_traineeapplications.ApplicationId={application_id}
            """    
        else:
            raise Exception("Blank values in the parameters")
            
        
        logger.info(f"[fetch_trainee_details_from_db] SQL Command: {command}")
        qs = cursor.execute(command)
        rows = cursor.fetchall()
        cols = [col[0] for col in cursor.description]
        result = [dict(zip(cols, row)) for row in rows]
        cursor.close
        logger.info(f"[fetch_trainee_details_from_db] SQL Result: {result}")
        print(result)
        return result

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.error(f"fetch_trainee_details_from_db {str(e)} at {str(exc_tb.tb_lineno)}")
        logger.info(f"[fetch_trainee_details_from_db] SQL Result: {None}")
        return None



def fetch_enrolled_trainee_details_summary_from_db(trainee_id=None):
    try:
        from django.db import connections
        cursor = connections['icici'].cursor()
        logger.info(f"[fetch_enrolled_trainee_details_summary_from_db] Trainee ID - RECEIVED - {trainee_id}")

        if trainee_id:
            # command = f"""
            # select l7_enrldtraineeapplication.TraineeId, l7_enrldtraineeapplication.TraineeName, 
            # l7_enrldtraineeapplication.BatchId, l7_enrldtraineeapplication.ISACourseId, l7_enrldtraineeapplication.Course, 
            # batchcalendar.BatchStartDate, batchcalendar.BatchEndDate, batchcalendar.Shift,
            # masterstaff.EmpId, masterstaff.EmpName, masterstaff.PhoneNo, masterstaff.Email,
            # l4_skillacademies.ISAId ,l4_skillacademies.ISAName ,l4_skillacademies.BuildingName ,l4_skillacademies.Address1,
            # l4_skillacademies.VillageTownCityName, l4_skillacademies.District ,l4_skillacademies.State ,l4_skillacademies.PinCode
            # from 
            # l7_enrldtraineeapplication inner join batchcalendar 
            # on 
            # l7_enrldtraineeapplication.BatchId=batchcalendar.BatchId 
            # and 
            # l7_enrldtraineeapplication.TraineeId={trainee_id} 
            # inner join 
            # masterstaff on batchcalendar.EmpId=masterstaff.EmpId
            # inner join
            # l4_skillacademies on batchcalendar.ISAId=l4_skillacademies.ISAId;"""
            command = f"""
                    select l7_enrldtraineeapplication.TraineeId, l7_enrldtraineeapplication.TraineeName,
                    l7_enrldtraineeapplication.BatchId, l7_enrldtraineeapplication.ISACourseId, l7_enrldtraineeapplication.Course,
                    l7_traineeapplications.Email as trainee_Email, l7_traineeapplications.PhoneNo as trainee_PhoneNo,l7_traineeapplications.DateOfBirth as trainee_DateOfB$
                    batchcalendar.BatchStartDate, batchcalendar.BatchEndDate, batchcalendar.Shift,
                    masterstaff.EmpId, masterstaff.EmpName, masterstaff.PhoneNo as emp_PhoneNo, masterstaff.Email as emp_Email,
                    l4_skillacademies.ISAId ,l4_skillacademies.ISAName ,l4_skillacademies.BuildingName ,l4_skillacademies.Address1,
                    l4_skillacademies.VillageTownCityName, l4_skillacademies.District ,l4_skillacademies.State ,l4_skillacademies.PinCode
                    from
                    l7_enrldtraineeapplication inner join batchcalendar
                    on
                    l7_enrldtraineeapplication.BatchId=batchcalendar.BatchId
                    and
                    l7_enrldtraineeapplication.TraineeId={trainee_id}
                    inner join
                    masterstaff on batchcalendar.EmpId=masterstaff.EmpId
                    inner join
                    l4_skillacademies on batchcalendar.ISAId=l4_skillacademies.ISAId
                    inner join
                    l7_traineeapplications on l7_enrldtraineeapplication.ApplicationId=l7_traineeapplications.ApplicationId;"""
        else:
            raise Exception("Blank values in the parameters")
        logger.info(f"[fetch_enrolled_trainee_details_summary_from_db] SQL Command: {command}")
        qs = cursor.execute(command)
        rows = cursor.fetchall()
        cols = [col[0] for col in cursor.description]
        result = [dict(zip(cols, row)) for row in rows]
        cursor.close
        logger.info(f"[fetch_enrolled_trainee_details_summary_from_db] SQL Result: {result}")
        return result

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.error(f"fetch_enrolled_trainee_details_summary_from_db {str(e)} at {str(exc_tb.tb_lineno)}")
        logger.info(f"[fetch_enrolled_trainee_details_summary_from_db] SQL Result: {None}")
        return None






'''

 ADDED NEW FUNCTIONALITY HERE 

'''

def check_input_trainee_application(rv):
    from .constants import course_id_dict,isa_id_dict
    if rv["FY"] != datetime.now().strftime("%y"):
        return False,"invalid FY value. Permitted Values 21,22,23,24,.. so on"

    elif int(rv["Salutation"]) != 1 and int(rv["Salutation"]) != 2 and int(rv["Salutation"]) != 3:
        return False,"invalid Salutation value. Permitted Values 1-(Mr.), 2-(Ms.), 3-(Mrs.)"
    
    elif len(rv["ISAId"]) != 3:
        return False,"invalid ISAId value. 3 digit value from 001 to 030"

    elif int(rv["Gender"]) != 1 and int(rv["Gender"]) != 2 and int(rv["Gender"]) != 3:
        return False,"invalid Gender value. Permitted Values 1-(Male), 2-(Female), 3-(Transgender)"


    elif rv["ISAName"] != isa_id_dict[rv["ISAId"]]["ISAName"]:
        return False,"invalid ISA Name value"

    elif len(rv["InterestedCourseId"]) != 2:
        return False,"invalid InterestedCourseId length. Permitted value 2 digit 01 to 31"

    elif rv["InterestedCourseId"] not in isa_id_dict[rv["ISAId"]]["AvailableCourses"]:
        return False,"Interested Course (Id & Course Name) not available for given ISA Id and ISA Location"

    elif rv["InterestedCourseName"] != course_id_dict[rv["InterestedCourseId"]]["CourseName"]:
        return False,"Invalid Course Name"

    elif rv["DateOfBirth"] != None:
        try:
            temp = datetime.strptime(rv["DateOfBirth"],"%Y-%m-%d")
            print(temp)
            return True, "Successfully Verified"
        except Exception as e:
            logger.error(f"Error in DateOfBirth {str(e)}")
            return False,"invalid DateOfBirth value. Please strictly follow the format YYYY-MM-DD. Example: \"27th August 1995\" --> \"1995-08-27\"" 
    else:
        return True, "Successfully Verified" 



def check_input_enrolled_trainee_application(rv):
    from .constants import course_id_dict,isa_id_dict,education_type_list, guardian_type_list, caste_type_list, religion_type_list, disability_type_list, annual_household_income_type_list,marital_status_type_list
    if len(str(rv["ApplicationId"])) != 10:
        return False,"Invalid ApplicationId value. Permissible ApplicationId value contains 10 digits."

    elif len(str(rv["BatchId"])) != 9:
        return False,"Invalid BatchId value. Permitted Values is of 9 digits "

    elif len(str(rv["ISACourseId"])) not in [5]:
        return False,"Invalid  ISACourseId value. Permitted value is of 5 digits. Please one leading 0 to make it 5 digit."

    elif int(str(rv["ISACourseId"])[-2:]) < 1 or int(str(rv["ISACourseId"])[-2:]) > 31:
        return False,"Invalid CourseId in ISACourseId"

    elif int(str(rv["ISACourseId"])[:3]) < 1 or int(str(rv["ISACourseId"])[-2:]) > 30:
        return False,"Invalid ISAId in ISACourseId"    

    elif int(rv["Gender"]) != 1 and int(rv["Gender"]) != 2 and int(rv["Gender"]) != 3:
        return False,"Invalid Gender value. Permitted Values 1-(Male), 2-(Female), 3-(Transgender)"

    elif int(rv["SameAsPermanentAddress"]) not in [1,0]:
        return False,"Invalid SameAsPermanentAddress value. Permitted Values 1-(Yes), 0-(No)"

    if len(str(rv["PPinCode"])) != 6:
        return False,"Invalid PPinCode value. Permissible PPinCode value contains 6 digits."

    elif rv["MaritalStatus"] not in marital_status_type_list:
        return False,"Invalid MaritalStatus value. Permitted values are Single, Unmarried, Married, Divorced, Widow"

    elif rv["GuardianType"] not in guardian_type_list:
        return False,"Invalid GuardianType value. Permitted values are S/o, D/o, W/o, C/o"

    elif rv["Caste"] not in caste_type_list:
        return False,"Invalid Caste value. Permitted values are General, SC, ST, OBC, PH, Others"

    elif rv["Religion"] not in religion_type_list:
        return False,"Invalid Religion value. Permitted values are Hindu, Muslim, Sikh, Jew, Christian, Buddhist, Jain, Others" 

    elif rv["DisabilityType"] not in disability_type_list:
        return False,"Invalid DisabilityType value. Permitted values are None, Blindness (Visually Impaired)), Locomotor Disability, Deaf, Low Vision, Hard of Hearing, Intellectual Disability, Autism Spectrum Disorder, Specific Learning Disabilities, Speech and Language Disability, Cerebral Palsy, Deaf and Blindness, Mental Behaviour,Mental Illness ,Mental Retardation, Leprosy Cured Patient, Acid Attack Victim, Dwarfism, Hemophilia, Thalassemia, Sickle Cell Disease, Multiple Sclerosis, Muscular Dystrophy, Parkinson Disease"

    elif int(rv["PreTrainingStatus"]) not in [1,2]:
        return False,"Invalid PreTrainingStatus value. Permitted Values 1-(Fresher), 2-(Experienced)"

    elif rv["EducationLevel"] not in education_type_list:
        return False,"Invalid EducationLevel value. Permitted values are Uneducated, Upto 4th, 5th to 8th, 9th to 10th , 11th to 12th , Undergraduate, Postgraduate, ITI, Polytechnic, Diploma"

    elif int(rv["AnnualHouseholdIncome"]) not in [1,2,3]:
        return False,"Invalid AnnualHouseholdIncome value. Permitted Values 1-(96 Thousand–2.5lakhs), 2-(Below 96 Thousand), 3-(Above 2.5 lakhs)"                 

    elif int(rv["BelowPovertyLine"]) not in [1,2]:
        return False,"Invalid BelowPovertyLine value. Permitted Values 1-Yes or 2-No"

    else:
        return True, "Successfully Verified"







def check_input_follow_up_enrolled_trainee(rv):
    from .constants import course_id_dict,isa_id_dict,education_type_list, guardian_type_list, caste_type_list, religion_type_list, disability_type_list, annual_household_income_type_list,marital_status_type_list
    if len(str(rv["TraineeId"])) != 11:
        return False,"Invalid TraineeId value. Permissible TraineeId value contains 11 digits."
    
    elif int(rv["WorkingStatus"]) not in [1,2]:
        return False,"Invalid WorkingStatus value. Permitted Values 1-(Working), 2-(Not Working)"

    elif int(rv["WorkingStatus"]) in [2] and int(rv["ReasonIfNotWorking"]) not in [1,2,3,4,5,6,7,8,9,10,11,12,13]:
        return False,"Invalid ReasonIfNotWorking value. Permitted values 1-(Job Profile), 2-(Distance), 3-(Employer Behaviour), 4-(Family Issues), 5-(Further Study), 6-(Marriage), 7-(Not interested in working), 8-(Reason not shared), 9-(Relocation), 10-(Self health), 11-(Timing Issue), 12-(Work Pressure), 13-(Others)"

    elif int(rv["WorkingStatus"]) in [2] and int(rv["ReasonIfNotWorking"]) in [13] and str(rv["OtherReason"]) in ["",None,"NULL","null"]:
        return False,"Invalid OtherReason value."
            

    elif len(str(rv["WorkingLocation"])) > 50:
        return False,"Invalid WorkingLocation value. Permissible WorkingLocation value contains max 50 characters."
        
    elif len(str(rv["MonthlySalary"])) > 20:
        return False,"Invalid MonthlySalary value. Permissible MonthlySalary value contains max 20 characters."
    
    else:
        return True, "Successfully Verified"
    
    
    

def get_batch_details(emp_id):
    response = {}
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
    
    
    return response
    
    
    
def get_batch_data(batch_id):
    response = {}
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
        
    return response


def get_custom_enrolled_trainee(isa_id , from_batch_start_date  , to_batch_end_date):
    
    from_batch_start_date = "2020-10-01"
    to_batch_end_date = "2020-12-01"
    
    response = {
            "status_code": 500,
            "message": "Internal server error"
            }
    try:
        if isa_id and from_batch_start_date and to_batch_end_date:
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
            batchcalendar.BatchEndDate >= \'{from_batch_start_date}\' and batchcalendar.BatchEndDate <= \'{to_batch_end_date}\';
            """
            logger.info(f"[GetCustomEnrolledTrainee] SQL Command: {command}")
            qs = cursor.execute(command)
            rows = cursor.fetchall()
            cols = [col[0] for col in cursor.description]
            result = [dict(zip(cols, row)) for row in rows]
            cursor.close
            logger.info(f"[GetCustomEnrolledTrainee] SQL Result: {result}")

        except Exception as e: 
            print(e)
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
    
    return response





def get_upcoming_batch_list(isa_id , course_id , batch_start_from_date , batch_start_to_date):
    response = {
            "status_code": 500,
            "message": "Internal server error"
    }
    try:

        print(isa_id)

        try:
            batch_start_from_date = batch_start_from_date
        except Exception as e:
            batch_start_from_date = None 

        try:
            batch_start_to_date =batch_start_to_date
        except Exception as e:
            batch_start_to_date = None  

        if isa_id and course_id and batch_start_from_date and batch_start_to_date:
            print(f"good to go")
        else:
            raise Exception("Invalid values in the request parameter(s).")    

        try:
            from django.db import connections
            cursor = connections['icici'].cursor()


            if int(course_id) == -1:
                command = f"""SELECT * FROM batchcalendar WHERE ISAId=\"{isa_id}\"
                and BatchStartDate >= \"{batch_start_from_date}\" and BatchStartDate <= \"{batch_start_to_date}\";
                """

            else:
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
        return response
    except Exception as e:
        print(e)


#Application id , phone no , email , dob , batch id , isa id , course id , trainee id 
#ApplicationId , PhoneNo , ISAId , TraineeId , TraineeName Course , BatchId , DateOfBirth , Email
def search_trainee(name , phone_no):
    response = {
            "status_code": 500,
            "message": "Internal server error"
    }
    try:
        from django.db import connections
        cursor = connections['icici'].cursor()
        command = f"""
        SELECT l7_traineeapplications.ApplicationId ,l7_traineeapplications.PhoneNo , l7_traineeapplications.ISAId ,
        l7_traineeapplications.BatchId, l7_traineeapplications.TraineeName , l7_traineeapplications.Email,
        l7_traineeapplications.DateOfBirth , l7_enrldtraineeapplication.Course ,  l7_enrldtraineeapplication.TraineeId
        FROM l7_traineeapplications 
        LEFT JOIN
        l7_enrldtraineeapplication
        ON
        l7_traineeapplications.ApplicationId = l7_enrldtraineeapplication.ApplicationId
        WHERE 
            l7_traineeapplications.PhoneNo="{phone_no}" OR l7_traineeapplications.TraineeName LIKE "%{name}%" LIMIT 50;;
        """
    
        logger.info(f"[search_trainee] SQL Command: {command}")
        qs = cursor.execute(command)
        rows = cursor.fetchall()
        cols = [col[0] for col in cursor.description]
        result = [dict(zip(cols, row)) for row in rows]
        cursor.close
        logger.info(f"[search_trainee] SQL Result: {result}")
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.error(f"search_trainee {str(e)} at {str(exc_tb.tb_lineno)}")
        logger.info(f"[search_trainee] SQL Result: {None}")
        return None
    
    if result != None:
        response['status_code'] = 200
        response['message'] = "Success"
        response['details'] = result
    else:
        response['status_code'] = 400
        response['message'] = "Bad request"
        response['details'] = result
    
    return response

# EmpId
# EmpName
# RoleName
# DepartmentName
# LocationName
# StateName
# ZoneName
# PhoneNo
# Email
# ReportingEmpName
# RoleName
# Email  


def get_gal_data(search_query = None , flag = -1):
    response = {
            "status_code": 500,
            "message": "Internal server error"
    }
    try:
        from django.db import connections
        cursor = connections['icici'].cursor()

        if search_query is None:
            command = f"""select * from  masterstaff e  INNER JOIN masterstaff m  ON m.ReportingEmpId = e.EmpId   LIMIT 1 ;"""
        
        elif search_query and flag == 0:
            #command = f"""select * from  masterstaff AS masterstaff1 WHERE EmpId  LIKE "%{search_query}%"  ;"""
            command = f"""select * from  masterstaff AS masterstaff1 INNER JOIN masterstaff AS masterstaff2  ON masterstaff1.EmpId = masterstaff2.ReportingEmpId   WHERE masterstaff2.EmpId  LIKE "%{search_query}%"  LIMIT 30  ;"""

        elif search_query and flag == 1:
            command = f"""select * from  masterstaff AS masterstaff1 INNER JOIN masterstaff AS masterstaff2  ON masterstaff1.EmpId = masterstaff2.ReportingEmpId  WHERE masterstaff2.EmpName  LIKE "%{search_query}%"  LIMIT 30  ;"""

            #command = f"""select * from  masterstaff WHERE Name  LIKE "%{search_query}%" ;"""
        else :
            command = f"""select * from  masterstaff AS masterstaff1 INNER JOIN masterstaff AS masterstaff2  ON masterstaff1.EmpId = masterstaff2.ReportingEmpId  WHERE masterstaff1.EmpName  LIKE   "%{search_query}%"  OR  masterstaff1.EmpId  LIKE  "%{search_query}%"  ;"""

            # command = f"""select * from  masterstaff WHERE Name  LIKE   "%{search_query}%"  OR  EmpId  LIKE  "%{search_query}%";"""


        logger.info(f"[get_gal_data] SQL Command: {command}")
        qs = cursor.execute(command)
        rows = cursor.fetchall()
        cols = [col[0] for col in cursor.description]
        result = [dict(zip(cols, row)) for row in rows]
        cursor.close
        logger.info(f"[get_gal_data] SQL Result: {result}")

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.error(f"get_gal_data {str(e)} at {str(exc_tb.tb_lineno)}")
        logger.info(f"[get_gal_data] SQL Result: {None}")
        return None
    
    if result != None:
        response['status_code'] = 200
        response['message'] = "Success"
        response['details'] = result
    else:
        response['status_code'] = 400
        response['message'] = "Bad request"
        response['details'] = result

    return response



def get_specific_gal(emp_id):
    response = {
            "status_code": 500,
            "message": "Internal server error"
    }
    try:
        from django.db import connections
        cursor = connections['icici'].cursor()

    except Exception as e:
        print(e)




def fetch_and_save_birthdays():
    response = {
            "status_code": 500,
            "message": "Internal server error"
    }
    try:
        from django.db import connections
        cursor = connections['icici'].cursor()
        command = f"""SELECT property_id FROM yourtable WHERE date IN (CURDATE() + INTERVAL 1 DAY)  """
        qs = cursor.execute(command)
        rows = cursor.fetchall()
        cols = [col[0] for col in cursor.description]
        result = [dict(zip(cols, row)) for row in rows]
        cursor.close
        logger.info(f"[get_gal_data] SQL Result: {result}")
    except Exception as e:
        print(e)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.error(f"get_gal_data {str(e)} at {str(exc_tb.tb_lineno)}")
        logger.info(f"[get_gal_data] SQL Result: {None}")
        return None
    
    if result != None:
        response['status_code'] = 200
        response['message'] = "Success"
        response['details'] = result
    else:
        response['status_code'] = 400
        response['message'] = "Bad request"
        response['details'] = result

    return response


def get_birth_days():
    currentDay = datetime.now().day
    currentMonth = datetime.now().month
    print(currentDay)
    print(currentMonth)

    if currentDay <= 9:
        currentDay = '0' + str(currentDay)
    if currentMonth <= 9:
        currentMonth = '0' + str(currentMonth)
    
    print(currentDay)
    print(currentMonth)

    response = {

            "status_code": 500,
            "message": "Internal server error"
    }
    try:
        from django.db import connections
        cursor = connections['icici'].cursor()
        command = f"""Select EmpId , EmpName ,DateOfBirth  from masterstaff where DateOfBirth LIKE '%{currentMonth}-{currentDay}%' AND ActStatus=1;"""
        qs = cursor.execute(command)
        rows = cursor.fetchall()
        cols = [col[0] for col in cursor.description]
        result = [dict(zip(cols, row)) for row in rows]
        cursor.close
        logger.info(f"[get_birth_days] SQL Result: {result}")

    except Exception as e:
        print(e)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.error(f"get_birth_days {str(e)} at {str(exc_tb.tb_lineno)}")
        logger.info(f"[get_birth_days] SQL Result: {None}")
        return None
    
    if result != None:
        response['status_code'] = 200
        response['message'] = "Success"
        response['details'] = result
    else:
        response['status_code'] = 400
        response['message'] = "Bad request"
        response['details'] = result

    return response




# SELECT l7_traineeapplications.*, l7_enrldtraineeapplication.TraineeId 
# FROM l7_traineeapplications 
# LEFT JOIN
# l7_enrldtraineeapplication
# ON
# l7_traineeapplications.ApplicationId = l7_enrldtraineeapplication.ApplicationId
# WHERE 
# l7_traineeapplications.PhoneNo="8302143337" OR l7_traineeapplications.TraineeName LIKE "Arpit%";


# Application id , phone no , email , dob , batch id , isa id , course id , trainee id 