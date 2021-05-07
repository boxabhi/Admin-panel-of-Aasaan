from os import name
from django.urls import path
from .views_api import *

urlpatterns = [
    path('trigger/' , Trigger , name="trigger"),
    path('source/' ,ImportSourcing ),
    path('assign-followups/' , AssignFollowups , name="assign"),
    path('store-batch-list/' , StoreBatchList , name="store_batch"),
    path('store-trainee-list/' , StoreTraineeList ),
    path('get-batch-details/' , GetBatchDetails ) ,
    path('issue-trainee-ceritficate/' , IssueTraineeCeritficate),
    path('download-users/' , DownloadUsers),
    path('import-user/' , ImportUsers),
    path('get-user-errors/' , GetUserErrors),
    path('application-id/' , FetchApplicantIdData),
    path('refresh/' , FetchApplicants),
    path('send_sms/' , SendSMS ),
    path('get-errors/' , GetErrors),
    path('remove/' , Remove),
    path('followup/' , ImportFollowUps),
    path('trigger-follow-ups' , TriggerFolowUps),
    path('enrollment/' , ImportEnrollments ),
    path('trigger-enrollments' , TriggerEnrollments),
    path('send-sms-email-to-pk/' , SendSMStoSpecificUser ),
    path('upload-users/' , UploadUsers),
    path('get-role-excel/' , GetRolesExcel),
    
    path('upload-file' , UploadFile),
    path('create-refferal/' , CreateRefferal),

    path('get-batch-list-api/' , GetBacthListApi),
    path('create-payment/' , CreatePayment),

    path('create-organization/' , CreateOrganization),
    path('create-financial-organization/' , CreateFinancialOrganization),
    path('create-certificate/' , CreateCertificate),

    path('upload-impact-excel/' , UploadImpactExcel),

    path('upload-job-posting-excel/' , UploadInternalJobPosting),

    path('create-job-posting/' , CreateJobPosting),

    path('update-job-posting/' , UpdateJobPosting),
]