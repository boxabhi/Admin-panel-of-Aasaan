from re import T
import re
from rolepermissions.roles import AbstractUserRole
from accounts.models import *



from functools import wraps
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied

from django import template




def has_permission_checker(permission_name , request):
    if request.user.is_superuser:
        return True

    # COMMENTED 

    # return True
    user_permissions = request.user.profile.permissions.all()
    if user_permissions.filter(permission_name = permission_name):
        return True
    raise PermissionDenied











permissions = [
    # users 
    'can_view_users',
    'can_manage_users',

    # reffral
    'can_view_reffral',
    'can_manage_reffral',

    #batches
    'can_view_batches',
    'can_manage_batches',

    #sourcing
    'can_view_sourcing',
    'can_manage_sourcing',

    #followups
    'can_view_followups',
    'can_manage_followups',

    #enrollments
    'can_view_enrollments',
    'can_manage_enrollments',
    #trainee
    'can_view_trainee',
    'can_manage_trainee',
    
    #followups
    'can_view_assigned_followups',
    'can_manage_trainee_followups',
]


class Admin(AbstractUserRole):

    admin_role_obj = Role.objects.filter(role_name = 'Admin').first()
    admin_permission_dict = {}

    for permission in admin_role_obj.permission.all():
        admin_permission_dict[permission.permission_name] = True
    available_permissions = admin_permission_dict

class SubAdmin(Admin):
    available_permissions = {
        'can_see_reports': True,
        'can_make_admin': True,
    }
    
    

class Manager(AbstractUserRole):
    available_permissions = {
        'view_followups' : True,
        'manage_trainee' : True,
        'view_users' : False,
    }
   
   
class Role1(AbstractUserRole):
    pass
    
    