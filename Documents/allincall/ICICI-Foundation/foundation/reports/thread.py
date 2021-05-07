

import time
import threading

from console.utils_api import fetch_trainee_details_from_db,fetch_enrolled_trainee_details_from_db
from console.utils import send_sms  , send_custom_mail
from .models import *
from django.conf import settings

from accounts.models import *
import xlrd
from django.dispatch import receiver
from asgiref.sync import async_to_sync
import json
import random
from channels.layers import get_channel_layer
import datetime
import os
from home.models import *

import sys
import logging
from django.conf import settings
import os
import pdfkit
import shutil
from django.conf import settings
logging.basicConfig()
logger = logging.getLogger(__name__)


class EmailAndSmsThread(threading.Thread):
    
    def __init__(self,objs ,subject ,email_message , message):
        self.objs = objs
        self.subject  = subject
        self.email_message = email_message
        self.message = message
        threading.Thread.__init__(self)
        
    def run(self):
        print('THREAD EXECUTED')
        try:
            message = self.message
            email_message = self.email_message
            subject = self.subject
            for obj in self.objs:
                if obj.contact_no:
                    if send_sms(obj.contact_no , message):
                        obj.sms_status = True

                if obj.email:
                    if send_custom_mail(obj.email,subject , email_message):
                        obj.email_status = True
                
                obj.save()
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error(f"EmailAndSmsThread {str(e)} at {str(exc_tb.tb_lineno)}")
          





class ImportUsersFromExcel(threading.Thread):
    def __init__(self,file_path ):
        self.file_path = file_path
        threading.Thread.__init__(self)
        
    def run(self):
        print('THREAD EXECUTED')
        try:
            wb = xlrd.open_workbook(self.file_path)
            sheet = wb.sheet_by_index(0)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error(f"import_source_from_excel {str(e)} at {str(exc_tb.tb_lineno)}")
            return [False], False

        
        rows = sheet.nrows - 1
        for i in range(rows):
            email_id = str(sheet.cell_value(i+1,1)).strip()
            emp_id = str(sheet.cell_value(i+1,2))
            first_name = str(sheet.cell_value(i+1,3)).strip()
            last_name = str(sheet.cell_value(i+1,4)).strip()
            raw_permissions = str(sheet.cell_value(i+1,4)).strip()

            profile_obj = Profile.objects.create(username = email_id , email = email_id  , emp_id =emp_id  , first_name = first_name  , last_name = last_name)
            profile_obj.set_password(f'ICICI@{email_id}')
        
            permissions = raw_permissions.split(',')

            for permission in permissions:
                role_obj = Role.objects.filter(role_name = permission).first()
                if role_obj:
                    profile_obj.role.add(role_obj)

            profile_obj.save()
            


class AddBatchesTodb(threading.Thread):
    def __init__(self,pk_lists ,batch_id):
        self.pk_lists = pk_lists
        self.batch_id = batch_id
        threading.Thread.__init__(self)
        
    def run(self):
        try:
            count = 0
            total = len(self.pk_lists)
            channel_layer = get_channel_layer()
            for pk_list in self.pk_lists:
                count += 1
                print(self.batch_id)
                # time.sleep(2)
                
                # async_to_sync(channel_layer.group_send)(
                # 'import',{
                #     'type': 'import_status',
                #     'value': json.dumps({'count' : count,'total' : total, }) 
                # })
                async_to_sync(channel_layer.group_send)(
                'order_%s' % self.batch_id,{
                'type': 'order_status',
                'value': json.dumps({'count':count,'total' : total})
                })
                print(count)
                if Batch.objects.filter(batch_id=pk_list['batch']).first() is None:
                    print((count / total) * 100) 
                    # Batch.objects.create(
                    #     batch_id = pk_list['batch'],
                    #     emp_id = pk_list['emp_id'],
                    #     batch_start = pk_list['batch_start_date'],
                    #     batch_end = pk_list['batch_end_date'],
                    # )    
        except Exception as e:
            print(e)    
    
    


class ImportPaymentFromExcel(threading.Thread):
    def __init__(self,file_path):
        self.file_path = file_path
        threading.Thread.__init__(self)
        
    def run(self):
        try:
            wb = xlrd.open_workbook(self.file_path)
            sheet = wb.sheet_by_index(0)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error(f"import_source_from_excel {str(e)} at {str(exc_tb.tb_lineno)}")
            return False, "Excel File Read Error"
        
        payment_objs = PaymentSheet.objects.filter(is_deleted =False)

        for payment_obj in payment_objs:
            payment_obj.is_deleted = True
            payment_obj.save()


        rows = sheet.nrows - 1

        excel_data = []
        for i in range(rows):
        
            ClaimNo   = str(sheet.cell_value(i+1,1)).strip() #
            IFIG_NO = str(sheet.cell_value(i+1,2)).strip()
            Inward = str(sheet.cell_value(i+1,3)).strip()
            Month = str(sheet.cell_value(i+1,4)).strip()
            Employee_Code = str(sheet.cell_value(i+1,5)).strip() #
            Inwarded_By = str(sheet.cell_value(i+1,6)).strip()
            Vendor_Code = str(sheet.cell_value(i+1,7)).strip()#
            Vendor_Name = str(sheet.cell_value(i+1,8)).strip()#
            Mail_Received_From = str(sheet.cell_value(i+1,9)).strip()
            Do_Name_PM_Name = str(sheet.cell_value(i+1,10)).strip()
            Claim_Type = str(sheet.cell_value(i+1,11)).strip()#
            From_Date = str(sheet.cell_value(i+1,12)).strip()
            To_Date = str(sheet.cell_value(i+1,13)).strip()
            Department = str(sheet.cell_value(i+1,14)).strip()
            PO_Number = str(sheet.cell_value(i+1,15)).strip()
            Invoice_No = str(sheet.cell_value(i+1,16)).strip()#
            Invoice_Date = str(sheet.cell_value(i+1,17)).strip()#
            Invoice_Amount = str(sheet.cell_value(i+1,18)).strip()#
            Ramco     = str(sheet.cell_value(i+1,19)).strip()
            Entry_Date     = str(sheet.cell_value(i+1,20)).strip()
            Authorised_Date     = str(sheet.cell_value(i+1,21)).strip()
            Entry_Done_By     = str(sheet.cell_value(i+1,22)).strip()
            USER_ID = str(sheet.cell_value(i+1,23)).strip()
            Payment     = str(sheet.cell_value(i+1,24)).strip()
        
            Upload_Number     = str(sheet.cell_value(i+1,25)).strip()
            UTR_NO     = str(sheet.cell_value(i+1,26)).strip()
            Payment_Date     = str(sheet.cell_value(i+1,27)).strip()
            UPLOAD_STATUS     = str(sheet.cell_value(i+1,28)).strip()
            STATUS     = str(sheet.cell_value(i+1,29)).strip()
            Remarks     = str(sheet.cell_value(i+1,30)).strip()
            Received_Date     = str(sheet.cell_value(i+1,31)).strip()
            Objection     = str(sheet.cell_value(i+1,32)).strip()
            Objection_Raised_By     = str(sheet.cell_value(i+1,33)).strip()
            Query     = str(sheet.cell_value(i+1,34)).strip()
            Resolution_Date     = str(sheet.cell_value(i+1,35)).strip()
            Resolution_By     = str(sheet.cell_value(i+1,36)).strip()
            Rejection_Date     = str(sheet.cell_value(i+1,37)).strip()
            Rejection_Done_By     = str(sheet.cell_value(i+1,38)).strip()
            Location     = str(sheet.cell_value(i+1,39)).strip()
            Classification     = str(sheet.cell_value(i+1,40)).strip()
            Reporting_Mngr     = str(sheet.cell_value(i+1,41)).strip()
            Zonal_Head     = str(sheet.cell_value(i+1,42)).strip()
            Zone     = str(sheet.cell_value(i+1,43)).strip()
            Period     = str(sheet.cell_value(i+1,44)).strip()
            Age     = str(sheet.cell_value(i+1,45)).strip()
            HGS     = str(sheet.cell_value(i+1,46)).strip()
        


            PaymentSheet.objects.create(
                    ClaimNo  =  ClaimNo,
                    IFIG_NO  =  IFIG_NO,
                    Inward  =  Inward,
                    Month  =  Month,
                    Employee_Code  =  Employee_Code,
                    Inwarded_By  =  Inwarded_By,
                    Vendor_Code  =  Vendor_Code,
                    Vendor_Name  =  Vendor_Name,
                    Mail_Received_From  =  Mail_Received_From,
                    Do_Name_PM_Name  =  Do_Name_PM_Name,
                    Claim_Type  =  Claim_Type,
                    From_Date  =  From_Date,
                    To_Date  =  To_Date,
                    Department  =  Department,
                    PO_Number  =  PO_Number,
                    Invoice_No  =  Invoice_No,
                    Invoice_Date  =  Invoice_Date,
                    Invoice_Amount  =  Invoice_Amount,
                    Ramco  =  Ramco,
                    
                    Entry_Date  =  Entry_Date,
                    Authorised_Date  =  Authorised_Date,
                    Entry_Done_By  =  Entry_Done_By,
                    USER_ID  =  USER_ID,
                    Payment  =  Payment,
                
                    Upload_Number  =  Upload_Number,
                    UTR_NO  =  UTR_NO,
                    Payment_Date  =  Payment_Date,
                    UPLOAD_STATUS  =  UPLOAD_STATUS,
                    STATUS  =  STATUS,
                    
                    Remarks  =  Remarks,
                    Received_Date  =  Received_Date,
                    Objection  =  Objection,
                    Objection_Raised_By  =  Objection_Raised_By,
                    Query  =  Query,
                
                    Resolution_Date  =  Resolution_Date,
                    Resolution_By  =  Resolution_By,
                    Rejection_Date  =  Rejection_Date,
                    Rejection_Done_By  =  Rejection_Done_By,
                    Location  =  Location,
                    Classification  =  Classification,
                    Reporting_Mngr  =  Reporting_Mngr,
                    Zonal_Head  =  Zonal_Head,
                    Zone  =  Zone,
                    Period  =  Period,
                    Age  =  Age,
                    HGS  =  HGS,
                    
            )










import pyqrcode
import png
from pyqrcode import QRCode

class IssueCertificateThread(threading.Thread):
    def __init__(self,objs):
        self.objs = objs
        threading.Thread.__init__(self)
        
    def run(self):
        from .helpers import random_sting
        try:
            print('@@')
            print(self.objs)
            print('@@')

            for obj in self.objs:
                name = obj.trainee_name
                application_id = obj.applicant_id
                trainee_id = obj.trainee_id

                certicate_id= str(random_sting(10))
                print(obj)
                print("SSS")

                s = f"{settings.DOMAIN_NAME}/media/certificates/QXVFNU2TW0.pdf"
                url = pyqrcode.create(s)

                url.png(f'{certicate_id}.png', scale = 6)

                shutil.move(str(settings.BASE_DIR) + f'/{certicate_id}.png' , str(settings.BASE_DIR) + f'/public/static/qr/{certicate_id}.png')
                print("oo")
                
               
                html_content = f"""
                        <!DOCTYPE html>
                        <html lang="en">
                        <head>
                            <meta charset="UTF-8">
                            <meta http-equiv="X-UA-Compatible" content="IE=edge">
                            <meta name="viewport" content="width=device-width, initial-scale=1.0">
                            <title>Ceriticate</title>
                            <link rel="preconnect" href="https://fonts.gstatic.com">
                            <link href="https://fonts.googleapis.com/css2?family=Open+Sans+Condensed:ital,wght@0,300;1,300&display=swap" rel="stylesheet">
                        </head>
                        <style>
                        </style>

                    <body style="font-size:25px;font-weight: bolder;letter-spacing: 1px;font-style: italic;font-family: 'Open Sans Condensed', sans-serif; background-color: rgb(243, 212, 198);margin: 0px;padding: 0px; ">
                        <div>
                            <div style="background-color: #005B75;height: 50px;width: 100%;"></div>
                            <div style="text-align: center;margin-top:80px">
                                <img src="https://icicifoundation.org/wp-content/uploads/2018/03/ICICI_Foundation_Logo.png">

                            </div>
        <div style="margin-top: 30px; text-align:center">
            <div style="background-position: center;background-image: url('https://icici-foundation-api.allincall.in/files/last.png');background-repeat:  no-repeat;   background-size:  800px;">
            <div style="opacity: 1 !important;display: flex;align-items: center;justify-content: center;
            "  >
                <img src="https://icici-foundation-api.allincall.in/files/Skill-India-Color.svg" style="height: 80px;margin-right: 30px;">
                <div class="vl" style="border-left: 2px solid #000;
                height: 80px; padding: 10px;"></div>
                <img src="https://icici-foundation-api.allincall.in/files/skill-development.svg" style="height: 80px;">
                      </div>
            <h2>Certificate Awarded to</h2>
            <h3 style="margin-top:10px"><i>{name}</i></h3>
            <p style="margin-top:10px">For completion of the </p>
            <p style="margin-top:10px">
                <b>
                    Vocational Skill Building Programme
                </b>
            </p>
                <h2 style="margin-top:10px;text-transform: uppercase;color:#B02A30">
                    Selling Skills - Using Digital Medium
                </h2>
                <p style="margin-top:10px"><i>
                        From {application_id}
                        To
                        {trainee_id}
                    </i> </p>    
                <p style="margin-top:10px"><b>
                        at <i>ICICI for Skills , Mumbai(TC130131)</i>
                    </b></p>
            </div>
        </div>
        <div style="margin-top:5px;text-align: center;">
            <h3 style="margin-top:-20px;padding: 0px;">Saurabh Singh</h3>
            <p style="margin-top:10px">President, ICICI Foundation for Inclusive Growth</p>
        </div>

        <p style="text-align:center ;margin-top:5px">
            This is a digital certificate. Authentication of the same can be done by scanning the QR code.
        </p>
        <div style="background-color: #005B75;height: 50px;width: 100%; margin-top: 200px;"></div>
        </div>
    </body>

    </html>
        """


            
            file_name =   certicate_id + '.pdf'
            #file_name = str(certicate_id) + '.pdf'
            
            Certificate.objects.create(
                trainee_id = obj,
                certificate_id = certicate_id,
                file_path = str(file_name)
            )

            pdfkit.from_string( html_content, file_name)
            
            #print('PDF GENERATED')
            shutil.move(str(settings.BASE_DIR) + f'/{file_name}' , str(settings.BASE_DIR) + f'/public/static/certificates/{file_name}')


        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error(f"import_source_from_excel {str(e)} at {str(exc_tb.tb_lineno)}")
            return False, "Excel File Read Error"