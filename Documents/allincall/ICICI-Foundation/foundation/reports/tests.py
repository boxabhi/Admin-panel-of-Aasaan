from django.test import TestCase

# Create your tests here.


from datetime import datetime
from random import randrange
from faker import Faker

from datetime import timedelta
import datetime
fake = Faker()

def generate_date():
    start = datetime.date(2020, 1, 1)
    end = datetime.date(2021, 2, 1)

    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)

from django.http import JsonResponse
def generate():
    for i in range(50):
        print(i)
        print(generate_date())
        Referral.objects.create(
        referrer_name = fake.name() , 
        referrer_mobile = fake.name(),
        referrer_email = fake.email(),
        referee_name =  fake.name() , 
        referee_mobile = fake.name() , 
        referee_email =  fake.email() , 
        source =  fake.name() , 
        created_at = generate_date(),
        )
        
        
    