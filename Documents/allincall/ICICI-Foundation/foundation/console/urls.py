
from django.urls import path

from . import views

urlpatterns = [

    path('', views.Home, name="home-views"),
    path('dashboard/' , views.dashboard , name="dashboard"),

    path('login/' , views.LoginAPI ),
    path('logout/' , views.logout_user , name="logout")
]
