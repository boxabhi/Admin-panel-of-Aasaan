from django.contrib import admin
from .models import *
from django.contrib.admin import DateFieldListFilter
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter

import datetime

class ReferralAdmin(admin.ModelAdmin):
    list_display = ["referrer_name" , "referee_name" , "created_at","updated_at"]
    
    list_filter = (
        #('created_at', DateFieldListFilter),
        ('created_at', DateRangeFilter), ('updated_at', DateTimeRangeFilter),
    )
    def get_rangefilter_created_at_default(self, request):
        return (datetime.date.today, datetime.date.today)

    # If you would like to change a title range filter
    # method pattern "get_rangefilter_{field_name}_title"
    def get_rangefilter_created_at_title(self, request, field_path):
        return 'Filter by created at'
    def get_rangefilter_updated_at_title(self, request, field_path):
        return 'Filter by updated at'

class OTPVerificationAdmin(admin.ModelAdmin):
    model = OTPVerification
    list_display = ["unique_otp_id","mob_no","email_id", "datetime"]
    list_filter = ('mob_no',"email_id")
    search_fields = ('unique_otp_id', 'mob_no', 'email_id', )

admin.site.register(OTPVerification, OTPVerificationAdmin)



admin.site.register(Referral , ReferralAdmin)