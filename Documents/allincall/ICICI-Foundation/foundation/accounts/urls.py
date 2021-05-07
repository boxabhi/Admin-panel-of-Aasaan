
from django.urls import path

from . import views
from . import views_api

urlpatterns = [

    path('login/' , views.show_login_page , name="show_login_page"),
    
    path('show/' ,  views.show_profile , name="profile"),

    path('roles/' , views.roles , name="roles"),


    path('update/' , views_api.UpdateProfile),
    path('upload_image/' , views.upload_image , name="upload_image"),

    path('toggle-active/' , views_api.ToggleActive),

    path('create-user/' , views_api.CreateUser),
    path('user/' , views_api.User , name="user"),
    path('delete/' , views_api.DeleteUser)

]
