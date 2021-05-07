
from django.urls import path

from . import views_api

urlpatterns = [
    # ICICI Foundation READ APIs
    path('get-batch-details/', views_api.GetBatchDetails, name="get-batch-details-api"),
    path('get-employee-details/', views_api.GetEmployeeDetails, name="get-employee-details-api"),
    path('get-skill-academy-details/', views_api.GetSkillAcademyDetails, name="get-skill-academy-details-api"),
    path('get-enrolled-trainee-details/', views_api.GetEnrolledTraineeDetails, name="get-enrolled-trainee-details-api"),
    path('get-trainee-details-by-mob-and-dob/', views_api.GetTraineeDetailsMobDob, name="get-trainee-details-api"),

    path('get-enrolled-trainee-details-summary/', views_api.GetEnrolledTraineeDetailsSummary, name="get-enrolled-trainee-details-summary-api"),

    # ICICI Foundation APIs WRITE APIs
    path('submit-trainee-application/', views_api.SubmitTraineeApplication, name="submit-trainee-application-api"),
    path('submit-enrollment-trainee-application/', views_api.SubmitEnrollmentTraineeApplication, name="submit-enrollment-trainee-application-api"),
    path('submit-follow-up-for-enrolled-trainee/', views_api.SubmitFollowUpEnrolledTrainee, name="submit-follow-up-for-enrolled-trainee-api"),

    # ICICI Foundation APIs Verification APIs
    path('send-mobile-otp/', views_api.SendMobileOTP, name="send-mobile-otp/-api"),
    path('send-email-otp/', views_api.SendEmailOTP, name="send-email-otp-api"),
    path('verify-otp/', views_api.VerifyOTP, name="verify-otp-api"),

    # ICICI Foundation APIs SEMI-WRITE APIs
    path('submit-referral/', views_api.SubmitReferral, name="submit-referral-api"),

    # ICICI Foundation APIs LOGIC BASED NEAREST LOCATION APIs
    path('find-nearest-academy/', views_api.NearestAcademy, name="find-nearest-academy-api"),
    
    
    
    path('get-batch-list/', views_api.GetBatchList, name="get-batch-list-api"),
    path('get-all-trainee-in-batch/', views_api.GetTraineeInBatch, name="get-all-trainee-in-batch-api"),
    path('get-custom-enrolled-trainee/', views_api.GetCustomEnrolledTrainee, name="get-custom-enrolled-trainee-api"),
    path('get-upcoming-batch-list/', views_api.GetUpcomingBatchList, name="find-nearest-academy-api"),


]
