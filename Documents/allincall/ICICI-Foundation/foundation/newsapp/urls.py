
from os import name
from django.urls import path
from .views import *

urlpatterns = [

    path('manage-news/' , manage_news , name="manage_news"),
    path('create-news/' , create_news , name="create_news"),
    path('update-news/<id>/' , update_news , name="update_news"),
    path('view-news/<slug>/' , view_news , name="view_news"),
    path('delete-news/' , DeleteNews),
    path('toggle-news-trending/' , ToggleNewsTrending),
    path('toggle-news-published/' , ToggleNewsPublished),

]