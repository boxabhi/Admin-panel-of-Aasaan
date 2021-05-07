from django.conf import settings
            



def check_valid_email(email):

    if email is None:
        return False

    domain_name = email.split('@')
    if domain_name[1] == "gmail.in":
        return True
    return False


def check_pincode_exists(pincode):
    from .pincode import pincode_list

    pincode_list = set(pincode_list)
    pincode = str(pincode)

    if pincode in pincode_list:
        return True
    return False
    


def get_pincode_details(pincode):
    from .pincode_dict import pincode_dict
    pincode = str(pincode)    
    return pincode_dict.get(pincode)
    
