from __future__ import print_function
from html.parser import HTMLParser
from reports.views import BASE_DIR
import string
import random
from html5lib.sanitizer import HTMLSanitizerMixin

from .models import *
import xlrd
from django.dispatch import receiver
from asgiref.sync import async_to_sync
import json
import random
from channels.layers import get_channel_layer
import datetime
import os
import time
import pyqrcode
import png
from pyqrcode import QRCode
from django.conf import settings
import os
import pdfkit
import shutil

class TestHTMLParser(HTMLParser):

    def __init__(self, *args, **kwargs):
        HTMLParser.__init__(self, *args, **kwargs)

        self.elements = set()

    def handle_starttag(self, tag, attrs):
        self.elements.add(tag)

    def handle_endtag(self, tag):
        self.elements.add(tag)
        
        

def send_updated(batch_id ,count , total ):
    channel_layer = get_channel_layer()
    print('send_updated called')
    increment_obj = IncrementBatchCounter.objects.get(socket_id = batch_id)
    increment_obj.current_count += 1
    async_to_sync(channel_layer.group_send)(
            'import',{
            'type': 'import_status',
            'value': json.dumps({'payload':'function end'})
        })
            

def store_batch_to_db(pk_lists , batch_id):
    count = 0
    channel_layer = get_channel_layer()
    total = len(pk_lists)
    increment_obj = IncrementBatchCounter.objects.get(socket_id = batch_id)
    for pk_list in  pk_lists:
        increment_obj.current_count += 1
        increment_obj.save()
        async_to_sync(channel_layer.group_send)(
            'order' ,{
                'type': 'order_status',
                'value': json.dumps({'count' : total , 'current' : increment_obj.current_count})
            }
        )
        if Batch.objects.filter(batch_id=pk_list['batch']).first() is None:
            Batch.objects.create(
                        batch_id = pk_list['batch'],
                        emp_id = pk_list['emp_id'],
                        batch_start = pk_list['batch_start_date'],
                        batch_end = pk_list['batch_end_date'],
                    )
        
        time.sleep(2)
     
        

   
    


def is_html(text):
    elements = set(HTMLSanitizerMixin.acceptable_elements)
    parser = TestHTMLParser()
    parser.feed(text)
    return True if parser.elements.intersection(elements) else False



def random_sting(N):
    res = ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k = N))
    return res


def convert_str_into_date(date_str):
    try:
        final_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        return final_date
    except Exception as e:
        print(e)

    return None

def save_qr_code(objs):
    pass





def save_pdf(objs , template_id , custom_course):
    print(objs)
    try:
        
        
        for obj in objs:
            name = obj.trainee_name
            application_id = obj.applicant_id
            trainee_id = obj.trainee_id

            certicate_id= str(random_sting(10))
            s = f"{settings.DOMAIN_NAME}/media/certificates/QXVFNU2TW0.pdf"
            url = pyqrcode.create(s)

            url.svg(f'{certicate_id}.svg', scale = 6)
            shutil.move(str(settings.BASE_DIR) + f'/{certicate_id}.svg' , str(settings.BASE_DIR) + f'/public/static/qr/{certicate_id}.svg')
            

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
            <img src="https://static.cdn.wisestamp.com/wp-content/uploads/2020/08/Thomas-Jefferson-autograph.svg-1024x637.png" style="height:120px">
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
            
            
            Certificate.objects.create(
                trainee_id = obj,
                certificate_id = certicate_id,
                file_path = str(file_name)
            )

            pdfkit.from_string( html_content, file_name)
            
            #print('PDF GENERATED')
            shutil.move(str(BASE_DIR) + f'/{file_name}' , str(BASE_DIR) + f'/public/static/certificates/{file_name}')

    except Exception as e:
        print(e)
    