
from django.urls import path
from .views import *

urlpatterns = [

    path('' , home  , name="home"),
    path('batches/' , batches , name="home_batches"),
    path('placement-partners/' , home_placement_partners  , name="home_placement_partners"),

    path('verify-ceriticate/' , verify_ceriticate , name="verify_ceriticate"),


    path('api/create-placement-partner/' , CreatePlacementPartners),
    path('api/create-schedule-interview/' , CreateScheduleInterview),
    path('api/create-tree-plantation/' , CreateTreePlantation),
    path('api/create-water-plantation/' , CreateWatershedData),

    path('api/add-remarks/' , AddRemarks)
    

]