from django.contrib import admin
from .models import *


admin.site.register(PlacementPartners)
admin.site.register(RequirementPlacementPartner)
admin.site.register(TreePlantation)
admin.site.register(WatershedData)
admin.site.register(TreePlantationPhotos)
admin.site.register(WatershedDataPhotos)

admin.site.register(PaymentUpload)
admin.site.register(PaymentSheet)