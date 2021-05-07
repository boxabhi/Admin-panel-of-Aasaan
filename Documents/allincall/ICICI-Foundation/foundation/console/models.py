from django.db import models

# Create your models here.
from django.utils import timezone   


class OTPVerification(models.Model):

    unique_otp_id = models.TextField(null=True, blank=True)
    
    otp = models.TextField(null=True, blank=True)
    
    mob_no = models.TextField(null=True, blank=True)
    email_id = models.TextField(null=True, blank=True)

    datetime = models.DateTimeField(default=timezone.now)

    failure_attempts = models.IntegerField(default=0)
    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.unique_otp_id

    class Meta:
        verbose_name = "OTPVerification"
        verbose_name_plural = "OTPVerifications"

class Referral(models.Model):

    referrer_name   = models.CharField(max_length=200,null=True, blank=True)
    referrer_mobile = models.CharField(max_length=200,null=True, blank=True)
    referrer_email  = models.CharField(max_length=100,null=True, blank=True)

    referee_name   = models.CharField(max_length=200,null=True, blank=True)
    referee_mobile = models.CharField(max_length=15,null=True, blank=True)
    referee_email  = models.CharField(max_length=100,null=True, blank=True)

    source         = models.CharField(max_length=100,null=True, blank=True)

    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return f"{self.referrer_name} - {self.referee_name}"

    class Meta:
        verbose_name = "Referral"
        verbose_name_plural = "Referrals"







class TodaysBirthDate(models.Model):
    emp_id = models.CharField(max_length=100)
    emp_name = models.CharField(max_length=100)

    