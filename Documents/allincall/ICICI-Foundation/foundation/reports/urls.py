
from os import name
from django.urls import path
from .views import *

urlpatterns = [

    path('batches/' , batches , name="batches"),
    path('students/<batch_id>/' , students , name="students"),
    path('referral/' , referral, name="referral"),
    
    path('users/' , show_users , name="show_users"),
    
    path('upload-users/' , upload_user_excel  , name="upload_user_excel"),    
    path('remove_upload_user/<id>' , remove_upload_user  , name="remove_upload_user"),

    path('sourcing/' , sourcing , name="sourcing"),
    path('enrollments/' , enrollments , name="enrollments"),
    path('followups/' , followups, name="followups"),

    path('view-enrollments/<id>/' , views_enrollments , name="views_enrollments"),
    path('view-followups/<id>/' , views_followups , name="views_followups"),
    path('view-sourcing/<id>/' , views_sourcing , name="views_sourcing"),


    path('manage-followups/' ,manage_followups , name="manage_followups"),
    path('assgined-followups/' , assigned_followups , name="assigned_followups"),
    path('view-assigned-followups/' , view_assigned_followups , name="view_assigned_followups"),
    path('<id>/show-assigned-followups/' , show_assigned_followups , name="show_assigned_followups"), 

   path('placement-partners/' , placement_partners , name="placement_partners"),

    path('create-trees/' , create_trees , name="create_trees"),
    path('create-water-data/' , create_watershed_data , name="create_watershed_data"),
    path('manage-water-data/' , manage_watershed_data , name="manage_watershed_data"),
    path('manage-trees-data/' , manage_trees_data , name="manage_trees_data"),
    path('scheduled-interviews' , scheduled_interviews , name="scheduled_interviews"),
    
    path('view-tree-plantation-images/<id>/' , view_tree_plantation_images , name="view_tree_plantation_images"),
    path('view-water-shed-images/<id>/' , view_water_shed_images , name="view_water_shed_images"),

    path('payments/' , payments , name="payments"),
    path('upload_payments/' ,upload_payments , name="upload_payments" ),

    path('search-payments/' , search_payments , name="search_payments"),

    path('filter-data/' , filter_data  , name="filter_data"),
    path('view-issue-ceritificate/' , view_issue_ceritficate  , name="view_issue_ceritficate"),


    path('add-organization/' , add_organization , name="add_organization"),
    path('manage-organization/' , manage_organization , name="manage_organization"),

    path('add-sessions/' , add_session , name="add_session"),
    path('manage-sessions/' , manage_session , name="manage_session"),

    path('create-certificate-templates/' , create_certificate_templates , name="create_certificate_templates"),

    path('manage-certificate-templates/' , manage_certificate_templates  , name="manage_certificate_templates"),

    path('show-certificate-template/<id>/' , show_certificate_template , name="show_certificate_template"),

    path('update-certificate-template/<id>/' , update_certificate_template  , name="update_certificate_template"),

    path('impact-upload/' , impact_upload , name="impact_upload"),

    path('gal/' , view_gal , name="view_gal"),
    path('gal/<emp_id>/' , view_detailed_gal , name="view_detailed_gal"),

    path('delete_uploaded_impact/<id>' , delete_uploaded_impact , name="delete_uploaded_impact"),
    path('show-hrms/' , show_hrms , name="show_hrms"),

    path('upload-internal-job-postings/' , upload_internal_job_postings ,name="upload_internal_job_postings"),
    
    path('update-job-posting/<id>/' , upload_job_posting , name="upload_job_posting"),
    path('delete-job-posting/<id>' , delete_job_posting , name="delete_job_posting" ),


    path('view_policy/<id>' , view_policy , name="view_policy")

]
