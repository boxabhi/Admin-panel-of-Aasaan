import re
from django.db import models
from django.contrib.auth.models import User, update_last_login



from django.contrib.auth.models import User
from django.db.models.expressions import F
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser



class Image(models.Model):
    image = models.ImageField(upload_to="profile")
    created_at = models.DateTimeField(null=True , blank = True , auto_now_add=True)
    updated_at = models.DateTimeField(null=True , blank = True , auto_now=True)






class Permissions(models.Model):
    permission_name = models.CharField(max_length=50)
    is_allowed = models.BooleanField(default=True)
    created_at = models.DateTimeField(null=True , blank = True , auto_now_add=True)
    updated_at = models.DateTimeField(null=True , blank = True , auto_now=True)
    def __str__(self):
        return self.permission_name


class Role(models.Model):
    role_name = models.CharField(max_length=100)
    permission = models.ManyToManyField(Permissions)
    created_at = models.DateTimeField(null=True , blank = True , auto_now_add=True)
    updated_at = models.DateTimeField(null=True , blank = True , auto_now=True)
    def __str__(self):
        return self.role_name

    


class User(AbstractUser):
    permissions = models.ManyToManyField(Permissions)

    def name(self):
        return self.first_name + ' ' + self.last_name


class Profile(User):
    profile_id = models.CharField(max_length=100 , null=True , blank=True , unique=True)
    dob = models.DateField(null= True , blank=True)
    address = models.TextField(null= True , blank=True)
    mobile = models.CharField(max_length=12 , null= True , blank=True)
    emp_id = models.CharField(max_length=100  , null=True , blank=True)
    profile_image = models.CharField(max_length=400 ,  null=True , blank=True)
    #is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(null=True , blank = True , auto_now_add=True)
    updated_at = models.DateTimeField(null=True , blank = True , auto_now=True)

    # def __init__(self, *args, **kwargs):
    #     super(User, self).__init__(*args, **kwargs)
    #     #self.role = ADMINISTRATOR_ROLE

    def save(self, *args, **kwargs):
        if self.pk == None:
            self.set_password(self.password)
        super(User, self).save(*args, **kwargs)

    # def delete(self, *args, **kwargs):
    #     super(User, self).delete(*args, **kwargs)

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profile'


    def check_admin_or_manager(self):
        if len(self.permissions.all()) == len(Permissions.objects.all()):
            return True
        return False
        


    def is_admin(self):
        if len(self.permissions.all()) == len(Permissions.objects.all()):
            return "Admin"
        return "User"

    def get_image(self):
        return self.profile_image



    def check_permission_for_template(self , permission_name):
        user_permissions = self.profile.permissions.all()
        if user_permissions.filter(permission_name = permission_name).first():
            return True
        return False





class UserUploadExcel(models.Model):
    file_path = models.TextField()
    total_entries = models.IntegerField(default=0)
    total_errors = models.IntegerField(default=0)
    errors_desc = models.TextField(default="[]",null=True , blank=True)
    is_imported = models.BooleanField(default=False)
    created_at = models.DateTimeField(null=True , blank = True , auto_now_add=True)
    updated_at = models.DateTimeField(null=True , blank = True , auto_now=True)
    def __str__(self):
        return self.file_path



# @receiver(post_save, sender=User)
# def save_profile(sender, instance , created, **kwargs):
#     if created:
#         try:
#             Profile.objects.get_or_create(user = instance)
#         except Exception as e:
#             print('profile already exixts')