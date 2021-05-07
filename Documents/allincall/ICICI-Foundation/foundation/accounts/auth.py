from .models import *


def check_admin_user(user):
    if len(user.role.all()) == len(Role.objects.all()):
        return True
    return False

def check_permission(user ,permission):
    roles = user.roles.all()
    for role in roles:
        if role == permission:
            return True
    return False
    
        