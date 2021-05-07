from enum import auto
from os import curdir
from re import I, M, T

from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models.expressions import F
from django.db.models.lookups import Transform
from .constants import *
import json

from django.contrib.auth import get_user_model
User = get_user_model()


class SourcingReportStatus(models.Model):
    user = models.ForeignKey(User , on_delete=models.SET_NULL , null=True)
    file_path = models.CharField(max_length=1000)
    total_entries = models.IntegerField(default=0)
    total_errors = models.IntegerField(default=0)
    errors_desc = models.TextField(default="[]",null=True , blank=True)
    current_status = models.IntegerField(default=0 ,  choices=STATUS)
    triggered_status = models.BooleanField(default=False)
    is_visible  = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add= True)


    def __str__(self):
        return self.user.username + f' created a file on  {self.created_at.strftime("%D-%m-%Y")}'

    def get_total_applicants(self):
        sourcing_objs = Sourcing.objects.filter(sourcing_report=self).exclude(application_id='[]')
        print(sourcing_objs)
        return len(sourcing_objs)     

    def download_file_path(self):
        file_path = (self.file_path).split('/')
        file_name = file_path[-1]
        return f'/media/{file_name}'
    
    def get_sent_message(self):
        sourcing_objs = Sourcing.objects.filter(sourcing_report=self , sms_status=True)
        return len(sourcing_objs)

    def get_sent_email(self):
        sourcing_objs = Sourcing.objects.filter(sourcing_report=self , email_status=True)
        return len(sourcing_objs)


    def get_current_status(self):
        if self.current_status == 0:
            return "Pending"
        elif self.current_status == 1:
            return "Uploaded"
        elif self.current_status == 2:
            return "Submitted"
        elif self.current_status == 3:
            return "Fetched Details"
        elif self.current_status == 4:
            return "Triggered SMS"
        elif self.current_status == 5:
            return "Completed"     





   


class Sourcing(models.Model):
    sourcing_report = models.ForeignKey(SourcingReportStatus , on_delete=models.CASCADE , null=True , blank=True)
    full_name = models.CharField(max_length=100)
    contact_no = models.CharField(max_length=12)
    email = models.EmailField()
    centre_name = models.CharField(max_length= 100)
    faculty_name = models.CharField(max_length= 100)
    sms_status = models.BooleanField(default=False)
    email_status = models.BooleanField(default=False)
    #sent_both_sms_email = models.BooleanField(default=False)
    application_id = models.TextField(default="[]", null=True , blank=True)
    #entry_created_by = models.CharField(max_length=100 , blank=True ,null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return self.full_name


    def get_application_id(self):
        if self.application_id == '[]':
            return "-"        
        data = json.loads(self.application_id)
        return data[0].get('id')
    
    def get_len_application_id(self):
        if self.application_id == '[]':
            return 0

        data = json.loads(self.application_id)
        return len(data)





#FollowUpReportStatus
# created_on
# updated_on

class FollowUpsReportStatus(models.Model):
    user = models.ForeignKey(User  , on_delete=models.SET_NULL , null=True)
    file_path = models.CharField(max_length=1000)
    total_entries = models.IntegerField(default=0)
    total_errors = models.IntegerField(default=0)
    errors_desc = models.TextField(default="[]",null=True , blank=True)
    current_status = models.IntegerField(default=0 ,  choices=STATUS)
    triggered_status = models.BooleanField(default=False)
    is_visible  = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return self.user.username + f' created a file on  {self.created_at}'   

    def download_file_path(self):
        file_path = (self.file_path).split('/')
        file_name = file_path[-1]
        return f'/media/{file_name}'
    
    def get_sent_message(self):
        sourcing_objs = FollowUps.objects.filter(follow_up_report=self , sms_status=True)
        return len(sourcing_objs)

    def get_sent_email(self):
        sourcing_objs = FollowUps.objects.filter(follow_up_report=self , email_status=True)
        return len(sourcing_objs)


    def get_current_status(self):
        if self.current_status == 0:
            return "Pending"
        elif self.current_status == 1:
            return "Uploaded"
        elif self.current_status == 2:
            return "Submitted"
        elif self.current_status == 3:
            return "Fetched Details"
        elif self.current_status == 4:
            return "Triggered SMS"
        elif self.current_status == 5:
            return "Completed"     

    def __str__(self):
        return self.user.username + f'created a file on {(self.created_at).strftime("%D-%m-%Y")}'

# FollowUp

class FollowUps(models.Model):
    follow_up_report = models.ForeignKey(FollowUpsReportStatus , on_delete=models.SET_NULL, null=True , blank=True)
    trainee_id = models.CharField(max_length=11)
    centre_name = models.CharField(max_length=100)
    faculty_name = models.CharField(max_length= 100)
    contact_no = models.CharField(max_length=12 , null=True , blank=True)
    email = models.EmailField(null=True , blank=True)
    sms_status = models.BooleanField(default=False)
    email_status = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add= True)


    def __str__(self):
        return self.trainee_id

class EnrollmentReportStatus(models.Model):
    user = models.ForeignKey(User  , on_delete=models.SET_NULL , null=True)
    file_path = models.CharField(max_length=1000)
    total_entries = models.IntegerField(default=0)
    total_errors = models.IntegerField(default=0)
    errors_desc = models.TextField(default="[]",null=True , blank=True)
    current_status = models.IntegerField(default=0 ,  choices=STATUS)
    triggered_status = models.BooleanField(default=False)
    is_visible  = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add= True)


    def __str__(self):
        return self.user.username + f' created a file on  {(self.created_at).strftime("%D-%m-%Y")}'   

    def download_file_path(self):
        file_path = (self.file_path).split('/')
        file_name = file_path[-1]
        return f'/media/{file_name}'
    
    def get_sent_message(self):
        enrollment_objs = Enrollments.objects.filter(enrollment_report=self , sms_status=True)
        return len(enrollment_objs)

    def get_sent_email(self):
        enrollment_objs = Enrollments.objects.filter(enrollment_report=self , email_status=True)
        return len(enrollment_objs)


    def get_current_status(self):
        if self.current_status == 0:
            return "Pending"
        elif self.current_status == 1:
            return "Uploaded"
        elif self.current_status == 2:
            return "Submitted"
        elif self.current_status == 3:
            return "Fetched Details"
        elif self.current_status == 4:
            return "Triggered SMS"
        elif self.current_status == 5:
            return "Completed"     




class Enrollments(models.Model):
    enrollment_report = models.ForeignKey(EnrollmentReportStatus , on_delete=models.SET_NULL , null=True)
    applicant_id = models.CharField(max_length=12 , null=True , blank=True)
    contact_no = models.CharField(max_length=12 , null=True , blank=True)
    email = models.EmailField(blank=True , null=True)
    sms_status = models.BooleanField(default=False)
    email_status = models.BooleanField(default=False)
    trainee_id = models.CharField(max_length=12 , null=True , blank=True)
    created_at = models.DateTimeField(null=True , blank = True , auto_now_add=True)
    updated_at = models.DateTimeField(null=True , blank = True , auto_now=True)

    def __str__(self):
        return self.applicant_id




class Trainee(models.Model):
    trainee_id = models.CharField(max_length=200 , null=True, blank=True)
    applicant_id = models.CharField(max_length=200 , null=True, blank=True)
    trainee_name = models.CharField(max_length=200 , null=True, blank=True)
    batch_id = models.CharField(max_length=100 , null=True, blank=True)
    is_certificate_issued = models.BooleanField(default=False)
    issue_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return self.trainee_name + ' | ' + self.trainee_id + ' | ' + self.batch_id


class Certificate(models.Model):
    trainee_id = models.ForeignKey(Trainee, on_delete=models.SET_NULL , null=T
     , blank=True)
    certificate_id = models.CharField(max_length=200 , null=True, blank=True)
    is_valid = models.BooleanField(default=False)
    is_approved =  models.BooleanField(default=False)
    file_path = models.TextField(null=True , blank=True)
    remarks = models.TextField(null = True , blank =True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.trainee_id.trainee_id + "  ceritificate issued - certificate number " + self.certificate_id
        

class Batch(models.Model):
    batch_id = models.CharField(max_length=100 , null=True, blank=True)
    emp_id = models.CharField(max_length=100  , null=True, blank=True)
    batch_start = models.CharField(max_length=100 , null=True, blank=True)
    batch_end = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True ,  null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True ,   null=True, blank=True)
    
    def __str__(self):
        return self.batch_id + '-' + self.emp_id

class BatchFollowups(models.Model):
    trainee_id = models.CharField(max_length=100)
    trainee_name = models.CharField(max_length=100)
    application_id = models.CharField(max_length=100)
    batch_id = models.CharField(max_length=100)
    isa_course_id = models.CharField(max_length=100)
    is_follow_up_done = models.BooleanField(default=False)
    follow_up_date_time = models.DateTimeField(null=True, blank=True)
    batch_start_date = models.CharField(max_length =100, null=True, blank=True)
    batch_end_date = models.CharField(max_length = 100  ,  null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True ,  null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True ,   null=True, blank=True)
    
    def __str__(self):
        return self.trainee_id
    



class BatchFollowUpsRecord(models.Model):
    assigned_to_user = models.ForeignKey(User ,related_name="assigned_to_user" ,  on_delete=models.SET_NULL ,  null=True, blank=True)
    assigned_by_user = models.ForeignKey(User, related_name="assigned_by_user" , on_delete=models.SET_NULL ,  null=True, blank=True)
    count_of_followups = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True ,  null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True ,   null=True, blank=True)
   
   
    def __str__(self):
        return self.assigned_by_user.username + f" assigned  {self.count_of_followups} followups to " + self.assigned_to_user.username


    
class UserBatchFollowups(models.Model):
    title = models.CharField(max_length=200 , null=True , blank=True)
    assign_to_user = models.ForeignKey(User, related_name="assigned_to"  , on_delete=models.SET_NULL ,  null=True, blank=True)
    assigned_by_user = models.ForeignKey(User, related_name="assigned_by" , on_delete=models.SET_NULL ,  null=True, blank=True)
    completion_date_for_followups = models.DateTimeField(null=True, blank=True)
    batch_followups = models.ManyToManyField(BatchFollowups)
    created_at = models.DateTimeField(auto_now_add=True ,  null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True ,   null=True, blank=True)
   


    def get_days_left(self):
        from datetime import datetime
        date_format = "%Y-%m-%d"
        a = (str(datetime.now())[0:10])
        b = (str(self.completion_date_for_followups)[0:10])
        # completetion_date = (str(self.completion_date_for_followups)[0:10])
        a = datetime.strptime(a, date_format)
        b = datetime.strptime(b, date_format)
        delta = b - a
        return str(delta.days)
        #return "Yo"
    
    

class FileUpload(models.Model):
    file = models.FileField(upload_to='files')


from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class IncrementBatchCounter(models.Model):
    socket_id = models.TextField()
    current_count = models.IntegerField(default=0)
    end_count = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

@receiver(post_save, sender=IncrementBatchCounter)
def increment_batch_count(sender, instance, **kwargs):
    increment_batch_obj = IncrementBatchCounter.objects.first()
    print('INSIDE SIGNAL')
    return
    
    channel_layer = get_channel_layer()
    if increment_batch_obj:
        print('Inside signal')
        print(increment_batch_obj.socket_id)
        increment_batch_obj.current_count += 1
        increment_batch_obj.save()
        async_to_sync(channel_layer.group_send)(
            'order' ,{
            'type': 'order_status',
            'value': json.dumps({'count':increment_batch_obj.current_count,'total' : increment_batch_obj.end_count})
        })




class FinancialOrganization(models.Model):
    name  =   models.CharField(max_length=100 , default="q", null=True , blank =True)
    organization_type  =   models.CharField(max_length=100 , null=True , blank =True)
    address  =   models.CharField(max_length=100 , null=True , blank =True)
    state  =   models.CharField(max_length=100 , null=True , blank =True)
    district  =   models.CharField(max_length=100 , null=True , blank =True)
    city  =   models.CharField(max_length=100 , null=True , blank =True)
    pincode  =   models.CharField(max_length=100 , null=True , blank =True)
    contact_person  =   models.CharField(max_length=100 , null=True , blank =True)
    designation  =   models.CharField(max_length=100 , null=True , blank =True)
    mobile  =   models.CharField(max_length=100 , null=True , blank =True)
    email  =   models.CharField(max_length=100 , null=True , blank =True)

    to_show = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class FinancialSession(models.Model):
    counsellor_name = models.CharField(max_length=100 , null=True , blank =True)
    program = models.CharField(max_length=100 , null=True , blank =True)
    isa = models.CharField(max_length=100 , null=True , blank =True)
    state = models.CharField(max_length=100 , null=True , blank =True)
    district = models.CharField(max_length=100 , null=True , blank =True)
    village = models.CharField(max_length=100 , null=True , blank =True)
    organization = models.ForeignKey(FinancialOrganization , on_delete=models.CASCADE , null=True , blank =True)
    mode = models.CharField(max_length=100 , null=True , blank =True)
    location = models.CharField(max_length=100 , null=True , blank =True)
    topics_covered = models.CharField(max_length=100 , null=True , blank =True)
    nature_of_participants = models.CharField(max_length=100 , null=True , blank =True)
    start_time = models.DateField(  null=True , blank =True)
    end_time = models.DateField(  null=True , blank =True)
    no_of_events = models.CharField(max_length=100 , null=True , blank =True)
    total_males = models.CharField(max_length=100 , null=True , blank =True)
    total_females = models.CharField(max_length=100 , null=True , blank =True)
    total_partipants = models.CharField(max_length=100 , null=True , blank =True)
    
    excel = models.FileField(upload_to="financial/excel" , null=True , blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class SessionImages(models.Model):
    financial_organization = models.ForeignKey(FinancialSession , on_delete=models.CASCADE)
    image = models.ImageField(upload_to="financial" , null=True , blank =True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)







class CertificateTemplates(models.Model):
    template_name = models.CharField(max_length=1000)
    content = models.TextField()
    to_show = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)




class ImpactBoxUpload(models.Model):
    file_path = models.TextField()
    is_imported = models.BooleanField(default=False)
    total_entries = models.IntegerField(default=0)
    errors = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return  self.file_path


class ImpactBox(models.Model):
    isa_total = models.CharField(max_length=100 , null=True , blank=True)
    isa_total_males = models.CharField(max_length=100 , null=True , blank=True)
    isa_total_females = models.CharField(max_length=100 , null=True , blank=True)
    isa_this_month_total = models.CharField(max_length=100 , null=True , blank=True)
    isa_males = models.CharField(max_length=100 , null=True , blank=True)
    isa_females = models.CharField(max_length=100 , null=True , blank=True)
    isa_this_fy_total = models.CharField(max_length=100 , null=True , blank=True)
    isa_this_fv_males = models.CharField(max_length=100 , null=True , blank=True)
    isa_this_fv_females = models.CharField(max_length=100 , null=True , blank=True)

    rl_total = models.CharField(max_length=100 , null=True , blank=True)
    rl_total_males = models.CharField(max_length=100 , null=True , blank=True)
    rl_total_females = models.CharField(max_length=100 , null=True , blank=True)
    rl_this_month_total = models.CharField(max_length=100 ,null=True , blank=True)
    rl_males = models.CharField(max_length=100 , null=True , blank=True)
    rl_females = models.CharField(max_length=100 , null=True , blank=True)
    rl_this_fy_total = models.CharField(max_length=100 , null=True , blank=True)
    rl_this_fv_males = models.CharField(max_length=100 , null=True , blank=True)
    rl_this_fv_females = models.CharField(max_length=100 , null=True , blank=True)


    rseti_total = models.CharField(max_length=100 , null=True , blank=True)
    rseti_total_males = models.CharField(max_length=100 , null=True , blank=True)
    rseti_total_females = models.CharField(max_length=100 , null=True , blank=True)
    
    rseti_this_month_total = models.CharField(max_length=100 , null=True , blank=True)
    rseti_males = models.CharField(max_length=100 , null=True , blank=True)
    rseti_females = models.CharField(max_length=100 , null=True , blank=True)
    rseti_this_fy_total = models.CharField(max_length=100 , null=True , blank=True)
    rseti_this_fv_males = models.CharField(max_length=100 , null=True , blank=True)
    rseti_this_fv_females = models.CharField(max_length=100 , null=True , blank=True)




    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def get_total(self):
        final_total = int(self.isa_total) + int(self.rl_total) + int(self.rseti_total)
        return final_total

    def get_total_males(self):
        final_total = int(self.isa_total_males) + int(self.rl_total_males) + int(self.rseti_total_males)
        return final_total

    def get_total_females(self):
        final_total = int(self.isa_total_females) + int(self.rl_total_females) + int(self.rseti_total_females)
        return final_total

    def get_total_month_total(self):
        
        final_total = int(self.isa_this_month_total) + int(self.rl_this_month_total) + int(self.rseti_this_month_total)
        return final_total

    def get_total_males_(self):
        final_total = int(self.isa_males) + int(self.rl_males) + int(self.rseti_males)
        return final_total

    def get_total_females_(self):
        final_total = int(self.isa_females) + int(self.rl_females) + int(self.rseti_females)
        return final_total

    def get_this_fy_total(self):
        final_total = int(self.isa_this_fy_total) + int(self.rl_this_fy_total) + int(self.rseti_this_fy_total)
        return final_total

    def get_this_fv_males(self):
        final_total = int(self.isa_this_fv_males) + int(self.rl_this_fv_males) + int(self.rseti_this_fv_males)
        return final_total

    
    def get_this_fv_females(self):
        final_total = int(self.isa_this_fv_females) + int(self.rl_this_fv_females) + int(self.rseti_this_fv_females)
        return final_total






from froala_editor.fields import FroalaField

        
class InternalJobPosting(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE ,null=True , blank=True )
    position = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    job_description = FroalaField()
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.position




class Policies(models.Model):
    policy_title = models.CharField(max_length=100)
    policy_description = models.TextField()
    policy_file = models.FileField(upload_to='policies')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.policy_title





