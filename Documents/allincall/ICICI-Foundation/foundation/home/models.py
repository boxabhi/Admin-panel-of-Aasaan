from enum import auto
from re import T
from django.db import models
from django.db.models.expressions import F
from django.db.models.lookups import Transform
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your models here.

class PaymentsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class PlacementPartners(models.Model):
    name_of_the_company = models.CharField(max_length=400)
    address_detail = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    name_of_person = models.CharField(max_length=100)
    designation_of_person = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    type_of_company = models.CharField(max_length=100)
    
    is_addressed = models.BooleanField(default=False)
    address_remarks = models.TextField(null=True , blank=True)
    addressed_by = models.ForeignKey(User , null=True , blank=True , on_delete=models.SET_NULL)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



    def __str__(self):
        return self.name_of_the_company



class RequirementPlacementPartner(models.Model):
    name_of_company = models.CharField(max_length=1000 , null=True ,  blank=True)
    location = models.CharField(max_length=100 , null=True ,  blank=True)
    course = models.CharField(max_length=100 , null=True ,  blank=True)
    designation = models.CharField(max_length=1000 , null=True ,  blank=True)
    salary = models.CharField(max_length= 1000 , null=True ,  blank=True)
    contact_person = models.CharField(max_length=1000 , null=True ,  blank=True)
    job_text = models.CharField(max_length= 100 , null=True ,  blank=True)
    job_description_file = models.FileField(upload_to='jobs' , null=True ,  blank=True)
    no_of_opening = models.CharField(max_length=100 , null=True ,  blank=True)
    created_at = models.DateTimeField(auto_now_add=True
    )
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f'{self.name_of_company}- {self.location} - {self.designation} - {self.salary} ' 







class TreePlantation(models.Model):
    date_of_plantation = models.CharField(max_length=100)
    isa_location = models.CharField(max_length= 100)
    no_of_trees = models.IntegerField()
    varieties = models.IntegerField()
    occasion = models.CharField(max_length=100)
    parternship = models.CharField(max_length=1000)
    staff = models.CharField(max_length=1000)
    post_plantation_care_by = models.CharField(max_length = 1000)
    
    def __str__(self):
        return self.isa_location


class TreePlantationPhotos(models.Model):
    tree_plantation = models.ForeignKey(TreePlantation , on_delete=models.CASCADE)
    file = models.FileField(upload_to='trees')

    def __str__(self):
        return   self.file.name






class WatershedData(models.Model):
    date =  models.CharField(max_length=100)
    name_of_school = models.CharField(max_length=1000)
    name_of_village = models.CharField(max_length=1000)
    block = models.CharField(max_length=1000)
    district = models.CharField(max_length=1000)
    terrace = models.CharField(max_length=1000)
    reservoir_type = models.CharField(max_length=1000)

    def __str__(self):
        return self.name_of_school

class WatershedDataPhotos(models.Model):
    water_shed_data = models.ForeignKey(WatershedData , on_delete=models.CASCADE)
    file = models.FileField(upload_to='water')

    def __str__(self):
        return  self.file.name

class PaymentUpload(models.Model):
    file_path = models.TextField()
    is_uploaded = models.BooleanField(default=False)
    entries = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PaymentSheet(models.Model):
    ClaimNo	  = models.CharField(max_length = 1000 , null = True , blank=True)
    IFIG_NO	  = models.CharField(max_length = 1000 , null = True , blank=True)
    Inward   = models.CharField(max_length = 1000 , null = True , blank=True)
    Date	  = models.CharField(max_length = 1000 , null = True , blank=True)
    Month	  = models.CharField(max_length = 1000 , null = True , blank=True)
    Employee_Code	  = models.CharField(max_length = 1000 , null = True , blank=True)
    Inwarded_By	  = models.CharField(max_length = 1000 , null = True , blank=True)
    Vendor_Code	  = models.CharField(max_length = 1000 , null = True , blank=True)
    Vendor_Name	  = models.CharField(max_length = 1000 , null = True , blank=True)
    Mail_Received_From	  = models.CharField(max_length = 1000 , null = True , blank=True)
    Do_Name_PM_Name	  = models.CharField(max_length = 1000 , null = True , blank=True)
    Claim_Type	  = models.CharField(max_length = 1000 , null = True , blank=True)
    From_Date	  = models.CharField(max_length = 1000 , null = True , blank=True)
    To_Date	  = models.CharField(max_length = 1000 , null = True , blank=True)
    Department	  = models.CharField(max_length = 1000 , null = True , blank=True)
    PO_Number	  = models.CharField(max_length = 1000 , null = True , blank=True)
    Invoice_No	  = models.CharField(max_length = 1000 , null = True , blank=True)
    Invoice_Date	  = models.CharField(max_length = 1000 , null = True , blank=True)
    Invoice_Amount	  = models.CharField(max_length = 1000 , null = True , blank=True)
    Ramco   = models.CharField(max_length = 1000 , null = True , blank=True)
    Document_No	  = models.CharField(max_length = 1000 , null = True , blank=True)
    Entry_Date	  = models.CharField(max_length = 1000 , null = True , blank=True)
    Authorised_Date	  = models.CharField(max_length = 1000 , null = True , blank=True)
    Entry_Done_By	  = models.CharField(max_length = 1000 , null = True , blank=True)
    USER_ID	  = models.CharField(max_length = 1000 , null = True , blank=True)
    Payment   = models.CharField(max_length = 1000 , null = True , blank=True)
    Details   = models.CharField(max_length = 1000 , null = True , blank=True)
    Submision_date	  = models.CharField(max_length = 1000 , null = True , blank=True)
    Upload_Number	  = models.CharField(max_length = 1000 , null = True , blank=True)
    UTR_NO	  = models.CharField(max_length = 1000 , null = True , blank=True)
    Payment_Date	  = models.CharField(max_length = 1000 , null = True , blank=True)
    UPLOAD_STATUS	  = models.CharField(max_length = 1000 , null = True , blank=True)
    STATUS	  = models.CharField(max_length = 1000 , null = True , blank=True)
    HGS   = models.CharField(max_length = 1000 , null = True , blank=True)
    Remarks	  = models.CharField(max_length = 1000 , null = True , blank=True)
    Objection  = models.CharField(max_length = 1000 , null = True , blank=True)
    Received_Date	  = models.CharField(max_length = 1000 , null = True , blank=True)
    Objection	  = models.CharField(max_length = 1000 , null = True , blank=True)
    Objection_Raised_By	  = models.CharField(max_length = 1000 , null = True , blank=True)
    Query   = models.CharField(max_length = 1000 , null = True , blank=True)
    Mail_Date	  = models.CharField(max_length = 1000 , null = True , blank=True)
    Resolution_Date	  = models.CharField(max_length = 1000 , null = True , blank=True)
    Resolution_By	  = models.CharField(max_length = 1000 , null = True , blank=True)
    Rejection_Date	  = models.CharField(max_length = 1000 , null = True , blank=True)
    Rejection_Done_By	  = models.CharField(max_length = 1000 , null = True , blank=True)
    Location	  = models.CharField(max_length = 1000 , null = True , blank=True)
    Classification	  = models.CharField(max_length = 1000 , null = True , blank=True)
    Reporting_Mngr  = models.CharField(max_length = 1000 , null = True , blank=True)	
    Zonal_Head	  = models.CharField(max_length = 1000 , null = True , blank=True)
    Zone	  = models.CharField(max_length = 1000 , null = True , blank=True)
    Period	  = models.CharField(max_length = 1000 , null = True , blank=True)
    Age	  = models.CharField(max_length = 1000 , null = True , blank=True)
    HGS   = models.CharField(max_length = 1000 , null = True , blank=True)
    Remark  = models.CharField(max_length = 1000 , null = True , blank=True)

    is_deleted = models.BooleanField(default=False)
    
    objects = PaymentsManager()
    admin_objects = models.Manager()


    def __str__(self):
        return str(self.id)
