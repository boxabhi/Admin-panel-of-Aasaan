from django.contrib import admin

# Register your models here.

from .models import *


admin.site.register(Role)
admin.site.register(Permissions)

admin.site.register(Profile)

admin.site.register(Image)
admin.site.register(UserUploadExcel)

