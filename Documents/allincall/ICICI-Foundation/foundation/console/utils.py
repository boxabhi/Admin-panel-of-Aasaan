from django.conf import settings
import sys
from math import radians, cos, sin, asin, sqrt
from random import randint
import requests
import json


import logging
logging.basicConfig()
logger = logging.getLogger(__name__)



def send_mail(from_email_id, to_emai_id, message_as_string, from_email_id_password):
    # from os.path import basename
    from email.mime.multipart import MIMEMultipart
    # from email.mime.application import MIMEApplication
    from email.mime.text import MIMEText
    from django.conf import settings
    import smtplib
    # # The actual sending of the e-mail
    server = smtplib.SMTP('smtp.gmail.com:587')
    # Credentials (if needed) for sending the mail
    password = from_email_id_password
    # Start tls handshaking
    server.starttls()
    # Login to server
    server.login(from_email_id, password)
    # Send mail
    server.sendmail(from_email_id, to_emai_id, message_as_string)
    print(f"Successfuly sent")
    # Close session
    server.quit()





def send_custom_mail(email,subject , message):
    from email.mime.multipart import MIMEMultipart
    # from email.mime.application import MIMEApplication
    from email.mime.text import MIMEText
    from django.conf import settings
    import smtplib
    global send_mail

    body = message
    
    """With this function we send out our html email"""
    to_emai_id = email

    from_email_id = settings.EMAIL_HOST_USER

    from_email_id_password = settings.EMAIL_HOST_PASSWORD

    email_message = MIMEMultipart('alternative')
    email_message['subject'] = subject 
    email_message['To'] = email
    email_message['From'] = from_email_id
    email_message.preamble = """"""

    # # Record the MIME type text/html.
    email_html_body = MIMEText(body, 'html')
    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    email_message.attach(email_html_body)

    try:
        send_mail(from_email_id, to_emai_id, email_message.as_string(), from_email_id_password)
        return True
    except Exception as e:
        return False




def send_otp_mail(email, otp):
    # from os.path import basename
    from email.mime.multipart import MIMEMultipart
    # from email.mime.application import MIMEApplication
    from email.mime.text import MIMEText
    from django.conf import settings
    import smtplib
    global send_mail

    body = """
    <head>
      <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
      <title>ICICI Foundation</title>
      <style type="text/css" media="screen">
      </style>
    </head>
    <body>
    <div style="padding:1em;border:0.1em black solid;" class="container">
        <p>
            Dear Applicant,
        </p>
        <p>
            {} is your verification OTP for ICICI Foundation. OTPs are secret. Do NOT disclose it to anyone.
        </p>
        <p>Kindly connect with us incase of any issue.</p>
        <p>&nbsp;</p>
        <p>Regards,</p>
        <p>ICICI Foundation for Inclusive Growth</p>
        
    </div>
    </body>""".format(otp)

    """With this function we send out our html email"""
    to_emai_id = email

    from_email_id = settings.EMAIL_HOST_USER

    from_email_id_password = settings.EMAIL_HOST_PASSWORD

    email_message = MIMEMultipart('alternative')
    email_message['subject'] = "ICICI Foundation - OTP Authentication"
    email_message['To'] = email
    email_message['From'] = from_email_id
    email_message.preamble = """"""

    # # Record the MIME type text/html.
    email_html_body = MIMEText(body, 'html')
    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    email_message.attach(email_html_body)
    print(f"Successfuly reached to send mail")
    try:
        send_mail(from_email_id, to_emai_id, email_message.as_string(), from_email_id_password)
        return otp
    except Exception as e:
        return -1



'''

ADDED FUNCTION HERE - 

'''


def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

def send_otp_at_given_mobile_number(mobile_number):
    OTP = random_with_N_digits(6)
    #MESSAGE = "Your authentication key is "+str(OTP)
    url=f"http://api.equence.in/pushsms?username=icici_found_otp&password=-EN20-sa&to=91{mobile_number}&from=IFOUND&text={OTP} is your verification OTP for ICICI Foundation. OTPs are secret. Do NOT disclose it to anyone."
    r= requests.get(url=url)
    json_data = json.loads(r.text)
    print(json_data)
    logger.info(json_data)
    if json_data["response"][0]["status"] == "success":
        print("checked ***************")
        return OTP
    else:
        return -1


def send_sms(mobile_number, message):
    url=f"http://api.equence.in/pushsms?username=icici_found_otp&password=-EN20-sa&to=91{mobile_number}&from=IFOUND&text={message}"
    #url=f"http://api.equence.in/pushsms?username=icici_found_otp&password=-EN20-sa&to=91{mobile_number}&from=IFOUND&text={message} ."
    print(url)
    r= requests.get(url=url)
    json_data = json.loads(r.text)
    print(json_data)
    logger.info(json_data)
    if json_data["response"][0]["status"] == "success":
        print("message sent successfully")
        return True
    else:
        return False





def distance(lat1,long1, lat2, long2):
    lat1, long1, lat2, long2 = map(radians, [lat1, long1, lat2, long2])
    dlon = long2 - long1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    km = 6371* c    
    return km
